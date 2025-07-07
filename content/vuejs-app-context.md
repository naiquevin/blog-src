Title: Async app context in Vue.js using promises
Author: Vineet Naik
Date: 2025-07-07
Tags: vuejs, frontend, captrice
Category: programming
Summary: How to initialize app context in Vue.js app using promises
Status: published

My guitar practice app, [Captrice](https://www.captrice.io) is built
using Vue.js. As a backend developer (although with some Backbone.js
experience from more than a decade ago), I chose Vue because it
allowed me to build quickly without having to learn the ever-evolving
libraries and tools in the frontend ecosystem today. I know my code
may not follow current best practices and I'm fine with it as long as
it's easy for me to reason about. I am the solo developer working on
the codebase and my top priority is maintainability. But as the app is
starting to grow in terms of features and complexity, it's time to
revisit some parts that can be optimized for performance and
extensibility.

The first thing I wanted to fix was redundant initialization of
IndexedDB client in router views. It was a bit too inefficient and
hacky for my comfort!

### The problem

Captrice is a local-only<a id="footnote-1-ref"
href="#footnote-1"><sup>1</sup></a> app that stores user data in the
browser's IndexedDB. In the early days there was only one top level
component for the practice interface and that was the entire app. But
soon the dashboard and library pages were added and routing was
introduced. The question was - how to have multiple router views use
the already initialized IndexedDB client? At that time I faced some
roadblocks due to my limited understanding of Vue and to avoid being
blocked on it for too long, I decided take the simplest approach
i.e. initializing the IndexedDB client in every router view component
that needed it. While it never caused any noticeable issues, it is
indeed redundant execution of code. When a user navigates from
practice page to dashboard page, the page doesn't reload in the
browser, so the db client object is already available in memory. Why
re-initialize it?

Had this been a backend application, I'd have moved the IndexedDB
client to something that I refer to as the "app context."

### App context in a frontend app

I don’t think "App context" is standard terminology. You may think of
it as the common resources or "global state" that's initialized when
an application starts, which can then be used during its life
cycle. Usual examples are database connections (or pool), caches, HTTP
clients etc. It's a very common pattern in backend apps, particularly
web apps.

As a backend dev, I can draw some similarities between a typical
backend app and a single page frontend application (SPA). Because SPAs
handle routing/navigation by themselves (instead of page refresh), the
term app context seems appropriate for the code that get initialized
once when the page loads.

### App context in a Vue app

App context is typically accessed through some form of dependency
injection. Let's take the example of a backend web app. At the time of
initializing the web server, an app context which is usually a kind of
hash map or dictionary is also initialized and passed to it. When an
incoming request is received, the framework invokes the handler
function, injecting the app context as an argument. Web frameworks
typically provide a way to associate handler functions with
routes. The handler functions of a backend web app can be loosely
mapped to the router views in Vue.

Dependency injection in Vue can be done either through props or the
[provide/inject](https://vuejs.org/guide/components/provide-inject)
API. In Captrice, props seem adequate as the context doesn't need to
be injected in deeply nested children components.

### Passing props from App.vue to the router views

One thing that tripped me when learning to use Vue was how passing
props from the root component i.e. App.vue to the router views is not
as straightforward as passing them from a regular Vue component to
it's child components.

In case of a component, a prop can be simply passed as,

```html
<!-- In App.vue -->
<MyComponent :colorScheme="colorScheme" />
```

In case of router view, additional syntax is required:

```html
<!-- In App.vue -->
<RouterView v-slot="{ Component }">
  <component :is="Component" :colorScheme="colorScheme" />
</RouterView>
```

Here, a prop named `colorScheme` is passed from `App.vue` to all the
router views that are rendered as it's child components. The value of
`colorScheme` is obtained from localStorage at page load and becomes
available in every router view that gets invoked as the user navigates
to the different "pages". Pretty straightforward.

What if we try to do the same for an IndexedDB wrapper? An important
difference is that the localStorage API is synchronous whereas
IndexedDB operations are asynchronous.

Sure, we can make the `created` lifecycle hook async and await inside
it. Using Vue's options API<a id="footnote-2-ref"
href="#footnote-2"><sup>2</sup></a>, it looks something like this:

```javascript
// In App.vue
export default {
  ...

  async created() {
    this.idb = markRaw(await initIndexedDb());
  },

  ...
}
```

And in App.vue's template,

```html
<!-- In App.vue -->
<RouterView v-slot="{ Component }">
  <component :is="Component" :idb="idb" />
</RouterView>
```

Finally, in all the router view components:

```javascript
// In router view component
export default {
  ...

  props: {
    idb: Object,
  },

  async created: {
    const data = await this.idb.fetchData();
  },

  ...
}
```

However, this doesn't quite work. While lifecycle hooks such as
`created` are allowed to be defined as async, Vue doesn't wait for the
async function calls in them to resolve. So this implementation will
likely result in an error that says `this.idb is null` in router
view's `created` hook, indicating that the IndexedDB client is not yet
initialized to be able to call methods on it.

Here's an illustration of a failure scenario:

```text
                           t0         t2                 t4
                            |          |      .           |
                            |          |      .           |
                            |----------|------.-----------|-------..
    created hook in App.vue |          |      .           |
                            |----------|------.-----------|-------..
                                       |      |           |
                               |-------.------|-----------.-------..
  created hook in Component    |       .      |           .
                               |-------.------|-----------.-------..
                               |       .      |           .
                               |       .      |           .
                              t1             t3

```

<u>t0</u>: The `created` hook of App.vue is invoked.

<u>t1</u>: The created hook of App's child component i.e. the router
view component is invoked. Despite the App's `created` hook being an
async function, Vue doesn't wait for the async calls in it to resolve
before proceeding with it's child components' lifecycle hooks.

<u>t2</u>: `await initIndexedDb()`is called in App's `created` hook (but
the promise resolves only at <u>t4</u>.

<u>t3</u>: `this.idb.fetchData()` is called in child component's
`created` hook but the promise returned by `initIndexedDb` in App's
`created` hook is not resolved yet. This means the value of the `idb`
prop is still null, resulting in an error.

<u>t4</u>: The promise returned by `initIndexedDb` resolves in App's
`created` hook, and only after this point, the `idb` prop in the child
component is usable.

It's easy to confirm the above by adding `console.log` statements.

### Passing promise as a prop

The above can be worked around by passing a prop that's a promise
instead of a value.

```javascript
// App.vue
export default {
  ...

  async created() {
    this.ctxPromise = new Promise(async (resolve) => {
      const idb = await initIndexedDb();
      resolve({
         idb: idb,
      });
    });
  },

  ...
}
```

In the router view's `created` hook, we await on the promise before
interacting with the database.

```javascript
// Router view component
export default {
  ...

  props: {
    appCtxPromise: Promise,
  },

  async created: {
    const appCtx = await this.appCtxPromise;
    this.idb = markRaw(appCtx.idb);
    const data = await this.idb.fetchData();
  },

  ...
}
```

Now it's guaranteed that before any db calls are made, the app context
and hence, the db object are initialized. An important thing to note
is that App's `created` hook should not `await` for some other promise
before the `ctxPromise` is created, otherwise the `appCtxPromise` prop
in router view's `created` hook could be null when trying to wait for
it to resolve.

This approach fixes the redundant execution of code, allows code reuse
and provides a framework for future additions to the app context, all
without using any external dependencies.

<hr/>

### Footnotes

<b id="footnote-1">1</b>. The goal is to be a local-first app, that
will sync user data with a backend, mainly for cross-device usability
and backups. However, in the current version users' data is only
stored locally in their browsers.<a href="#footnote-1-ref">&#8617;</a>

<b id="footnote-2">2</b>. The composition API seems to be more widely
recommended, but I find the options API easy to reason about and work
with. <a href="#footnote-2-ref">&#8617;</a>

