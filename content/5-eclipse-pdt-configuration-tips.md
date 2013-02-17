Title: 5 Eclipse PDT configuration tips
Author: Vineet Naik
Date: 2009-12-17 17:51:20
Tags: code templates, Eclipse PDT, php, web development, www.kodeplay.com
Category: Eclipse PDT
Summary: 

Update: I have stopped using Eclipse and moved to Emacs

Last friday as we resumed the daily knowledge sharing sessions at [kodeplay](http://www.kodeplay.com/), it was my turn first up and my topic for the day was eclipse & svn. For those who are not familiar, [Eclipse PDT](http://www.eclipse.org/pdt/) (PHP development tools) is an excellent IDE for php development and someone who is looking to move up from a normal editor to an IDE must certainly consider trying it out.

For those who are already fans of PDT like me and who are using it, I am going to share a few tips and discoveries that will make your life easy.<!--more-->

1. **Choose only what Eclipse must load**: Eclipse is not doubt slow to start and the reason for this is that it loads various plugins and components while starting up. But you may not be using all of them unless you already live and breathe PDT! (and that should be having me asking for tips.) A few I prefer not to load are the ones related to usage data gathering and automatic updates. To switch off the unnecessary plugins goto,
   Window>Preferences>General>Startup & shutdown and uncheck the ones you don't require.

2. **Refreshing the workspace**: The eclipse workspace doesn't refresh automatically by default which means that if I create a folder inside my project from outside (say using windows explorer), eclipse will not show the changes till i press F5 (refresh manually.) To save the trouble we can do one of the two things depending upon how we like to use the editor. The first way is to ask Eclipse to refresh on every start up. To do this follow exactly the same path as in tip #1 and select the "refresh workspace on startup" checkbox. The second way is to ask eclipse to keep refreshing the workspace. To enable this goto,
   Window>Preferences>General>Workspace and select the refresh automatically option.

3. **Associate other file types with the editor**: If you work with files other than .php such as .tpl, then viewing the file in the editor will remind you of notepad. Personally I like my javascript to be easily noticeable within the html and php code which will not happen in tpl files by default. To restore the colourfulness :), you will have to associate the file type with content type, ( here *.tpl with php content.)  Goto*** Preferences>General>Content types***. Select *text* > *php content type*. Add a new file type here (*.tpl) and then reload all the tpl files for the effect to be seen.

4. **Using Code templates**: If you follow a certain pattern while writing code (I believe every one of us do and to clarify, following a pattern doesn't necessarily mean code duplication) then knowing this setting is bound to change your life. For all the code that you keep typing again and again will be stored as a template and can be pasted in to the code using just typing out its name. For using templates first  go to ***Preferences>PHP>editor>templates***. A list of templates can be seen. Clicking on specific names will load the preview. Using the add button, add new templates and forget the code for ever!
   for eg. add a new template for writing a small comment like,
   /* code edited by vineet */
   and then wherever required, just type in the name and press *ctrl+space* and allow the magic to happen.

5. **Filter the Resource: **The final tip will help a lot if you keep multiple projects in one workspace and even more if you have multiple platforms based projects in the same workspace for eg. two[ wordpress](http://wordpress.org/) based blogs. By pressing ***ctr+shift+r***, we can *open the resource* to find a particular file. Suppose I want to find a commonly found file called "style.css" and the workspace has wordpress, opencart installations and some other projects in my own code then the open resource will show me a list of "style.css" files which will, instead of doing any good, actually bring me to the initial point . So, in order to filter the resource and keep it confined to a particular project or folder, do an "open resource" and click on the downward arrow on the right top. Create a new *working set there *and select it by clicking on the arrow again. Now eclipse will search only the working set and return specific results.

Hope these tips will save you from some everyday trouble. Will try to share more such PDT related discoveries. Helpful tips from your side by the way of comments are most welcome :)