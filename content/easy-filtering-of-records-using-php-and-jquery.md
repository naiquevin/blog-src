Title: Easy filtering of records using PHP and JQuery.
Author: Vineet Naik
Date: 2010-01-05 18:11:05
Category: jquery, php
Summary: 

I came upon a method for filtering records using jquery and php. I am
sure there must be plugins available to do this but this one is super
easy. Particularly for problems where the elements are to be filtered
by multiple criteria and each element falls in more than one criteria
at a time. Consider the following problem.

An e-commerce app (a typical online store) has 10 products in 4
categories and each product can be present in more than one category
at a time. All these products are to be shown as a list or in rows of
an html table. Then they have to be filtered by categories (which
means when i select a particular category from a list of categories in
a drop down, only those products which are categorized under it should
appear and the others should not show.)

The method i came up with is this.

Get data from the database using php (or for that matter any server
side scripting language)

1. an array of all the products 
2. an array of all the categories that the product falls under

The above data can be actually fetched into a single associative array
for ease of looping

```php
    <?php
    $products[] = array(
        'product_id' => 1,
        'name'=> 'ipod',
        'in_categories' => array(2,3,5,6)
    );
```

Then loop through the above array to show the products in a table and
add multiple classes to the tr that represents each product depending
upon the categories under which the product falls.

```php
    <table border="0" cellspacing="0" cellpadding="0">
        <?php  foreach($products as $product){  ?>
            <tr class="c_all <?php foreach($product['in_categories'] as $cat){ echo 'c_' . $cat . ' '; } ?>"> 
            <!-- don't forget that space after each class -->
                <td></td>
                <td></td>
                <td></td>
            </tr>
        <?php } ?>
    </table>
```

Once this is done, filtering is just a matter of writing a javascript
function and calling it on the onChange event of the category drop
down box.

```javascript
    function filterProducts(byCat){
        $("c_"+all).hide(); // first hide all records
        $("c_"+byCat).show(); // show records of the category
    }
    //calling the function to show products under category 2
    $("#filter").click(function(){
        filterProducts(2);
    });
    // to show all the products back again
    filterProducts('all');    
    // if your application allows adding adding ,removing or moving
    // products from one category to another using ajax    
    $("#product_"+productId).addClass("c_"+catId);
    $("#product_"+productId).removeClass("c_"+catId);
```

Advantages of the above method:

1. no ajax requests as all the data is already there.
2. at any time a product can be added to (or removed from) a
   particular category by using the addClass and removeClass functions of
   jquery and it will work perfectly for the later onchange events.

Disadvantages:

1. I am not sure what effects if will have on performace.
2. For now, I am leaving aside the jquery performance issues but i
   think heavy looping in jquery must be better than making ajax requests
   to the server.

I hope someone will find this helpful. If you know any other alternate
method for this then please share by commenting on this post. All-hail
JQuery!
