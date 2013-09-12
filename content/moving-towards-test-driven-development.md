Title: Moving towards Test Driven Development
Author: Vineet Naik
Date: 2010-12-14 17:48:28
Category: testing
Summary: Using Poor man's TDD techniques

Recently, I have been reading a lot about Unit Testing and other stuff
related to Test Driven Development. What generates an interest is that
the idea itself looks promising and totally convinces me. Something
that will, upon a single command tell if everything is upto the mark
at any given time is beyond any doubt a sure shot #win! Also, in all
the online articles and the subsequent discussions that I have read
about TDD, I haven't come across even one "why-TDD-is-bad" or
"has-a-downside" argument.

I believe that by default, it doesn't take much time for a developer
to realize that testing is an integral part of development. Right from
the first "hello world" to that impressive little facebook app you
just rolled out, every application goes through
let-me-first-see-if-it-works phase before its shown to friends and
colleagues. Developers at all levels of skills, expertise and
experience have to test their code.

As a beginner I wanted all things to work. At times my code passed the
test, then I changed something that broke it, which meant testing it
all over again and that was just frustrating. I wonder what would have
been my first opinion about TDD if I had read it then. Because as I
see it, TDD is about how to use those dreaded terms such as *Fatal
Error*, *Notice*, *Warning,* and even worst, *An Uncaught Exception
*to your advantage. Nevertheless from my experience, I believe that
with more and more coding, we naturally come up with our own
convenient testing techniques and tricks. What I have observed is that
in a way it brings us close to the concept of Unit Testing and TDD.

One and probably my first such self discovered trick was testing
callback functions of ajax requests in javascript. It involves not
making the ajax request at all at first and directly calling the code
that would have been the call back of the request. The function takes
an argument that later on would be replaced by the actual server
response. Say for example, I need to post a form by making an ajax
request.

```javascript
    $("#submit").click(function (resp) {
        if(1 == resp.status) {
            alert('done!');                 
        } else {          
            alert('failed!');
        }
    });
```

Once this thing passes, my only concern is that the server response
should get me ``status = 0`` if something goes wrong and ``status =
1`` if everything works fine. Then there is no need to test the
callback code, which in actual scenario, would obviously be more
complex.

Another trick I discovered was that instead of making a thousand
clicks to test server side code, its far more convenient to create a
dummy action in your controller (I mostly use the zend framework)
where the CRUD will be first tested before it goes into its dedicated
action. This gives a lot of confidence because the code will be dealt
with a lot of test cases while it is still in the dummy action. To
relate this example with the previous one,

```php
    <?php
    public function dummyAction () {
        $post = array(
            'name' => 'vineet', 
            'password' => 'helloworld'
        );    
        $resp = array();    
        if (doSomething($post)) {
            $resp['status'] = 1;
        } else {
            $resp['status'] = 0;
        }    
        echo Json::encode($resp);    
        //stop zf from looking for a view for this action and show result in browser for now    
        exit; 
    }
```

So now just navigate to this dummy action and see if its working. Then
test it for different set of inputs until you feel confident
enough. No need to say that the next step is to connect these two
segments of throughly tested code. This also saves us from a lot of
debugging from the firebug console.

But after using this technique for a while, I felt something was wrong
about this method. The code inside the dummy action was shortlived as
very soon it would get replaced by fresh code that needed to be
tested. This was resolved by creating a dedicated controller for all
my tests which would of course be actions that would stay in the
controller for further testing. This method also allows directly
testing other actions in the same or different controllers thanks to
the ``forward`` method of the ``Zend_Controller_Action``. Also to avoid
writing duplicate code for setting global variables, I created a
simple class that acts as a Helper to the TestController

```php
    <?php
    class MyTestHelper {
        public function mergePost ($data) {
            $_POST = array_merge($_POST,$data);
        }
        public function mergeGet ($data) {
    
        }
    }
```

Then create our TestController that will hold all the tests.

```php
    <?php    
    class TestController extends Zend_Controller_Action {
        public function preDispatch () {
            $this->testHelper = new MyTestHelper();
        }
        public function testcontactformAction () {
            $this->testHelper->mergePost(array(
                'email'=>'fake@email.com',
                'comment'=>'test comment'
            ));
            //forward it to where the actual action happens (pun intended!)
            $this->_forward('contactform','index');
        }
    }    
```

Whenever something needs to be tested, I just look up this controller
for the test action and run it in the browser. It also makes
refactoring hastle free to some extent.

An important point to note is that error reporting must be turned on
for this to work.

```php
    <?php    
    error_reporting(E_ALL | E_STRICT);
    ini_set("display_errors","on");
```

Although these methods have many limitations and are very raw as
compared to testing frameworks such as phpUnit, it works for me at the
moment. Regarding phpUnit, I feel its a great tool. I do use it for
testing utility functions and methods that don't involve fetching and
saving to the database. I have read phpUnit can manage that, just need
to sit down some time and try it out.
