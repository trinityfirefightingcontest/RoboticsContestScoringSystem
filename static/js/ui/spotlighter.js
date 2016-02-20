define(["jquery", "lodash"], function($, _) {
           
           var highlightClass = "spotlight-highlight";

           var isActionKey = function(keyCode) {
             return (keyCode === 40 || keyCode === 38 || keyCode === 9 || keyCode === 13);
           };

           var highlightItem = function(currentHighlight, $output, nextMethod) {
               if ($output.children().filter(":visible").length > 1) {
                   var isNext = nextMethod === "next";
                   var nextHighlight = isNext ? currentHighlight.nextAll(":visible:first") 
                       : currentHighlight.prevAll(":visible:first");
                   currentHighlight.removeClass(highlightClass);
                   if(nextHighlight.length > 0) {
                       nextHighlight.addClass(highlightClass);
                   } else {
                       var _elem = $("> :visible", $output).first();
                       if(!isNext) {
                           elem = $("> :visible", $output).last();
                       }
                       _elem.addClass(highlightClass);
                   }
               }
           };

           var handleActionKeys = function($output, keyCode, shiftKey) {
               var currentHighlight = $("." + highlightClass, $output);
               // simulate click on highlighted item when 'enter' key is pressed
               if(keyCode === 13) {
                   $("a", currentHighlight)[0].click();
               }
               // highlight next item when 'down' or 'tab' key is pressed
               if(keyCode === 40 || (!shiftKey && keyCode === 9)) {
                   highlightItem(currentHighlight, $output, "next");
               }
               // highlight previous item when 'up' or 'shift+tab' key is pressed
               if(keyCode === 38 || (shiftKey && keyCode === 9)){
                   highlightItem(currentHighlight, $output, "prev");
               }
           };

           var handleKeyPress = function($input, $output, $showAll, e) {
               var inputText = $input.val().replace(/^\s+|\s+$/g, '');
               var searchText = inputText.replace(/[\s\\\(\)\[\]\*]+/, " ").replace(/^\s+|\s+$/g, "");
               var searchTextTokens = searchText.split(" ");
               var searchTextRegexp = "[\\s|^]" + searchTextTokens.join(".*\\s");
               var searchRegExp = new RegExp(searchTextRegexp, "i");
               $("~ span", $output).remove();
               if (searchText) {
                   $showAll.hide();
                   var hideOrShowRelevantChild = function(i) {
                       var textHit = searchRegExp.test($(this).text().replace(/\W+/g, " "));
                       var $this = $(this);
                       if(textHit) {
                           $this.show();
                       } else {
                           $this.hide();
                       }
                   };
                   $output.children().each(hideOrShowRelevantChild);
                   if(!isActionKey(e.keyCode)) {
                       $("." + highlightClass, $output).removeClass(highlightClass);
                       $(":visible:first", $output).addClass(highlightClass);
                   }
                   if ($("> :visible", $output).length < 1) {
                       $output.after("<span class='spotlight-error'>No robots matching your query</span>");
                   }
               } else {
                   $showAll.show();
                   var children = $output
                       .children()
                       .sort(function(a, b) {
                                 var rankA = parseInt($(a).attr("data-rank"), 10);
                                 var rankB = parseInt($(b).attr("data-rank"), 10);
                                 return (rankA < rankB) ? -1 : (rankA > rankB) ? 1 : 0;
                             });
                   $output.html(children);
                   $("> *:lt(5)", $output).show();
                   $("> *:gt(4)", $output).hide();
                   if(!isActionKey(e.keyCode)) {
                       $("." + highlightClass, $output).removeClass(highlightClass);
                   }
               }
           };

           var interceptActionKeys = function($output, e) {
               if (isActionKey(e.keyCode)) {
                   handleActionKeys($output, e.keyCode, e.shiftKey);
                   e.preventDefault();
               }
           };
           
           var showAllChildren = function($output) {
               $output.children().show();
               $(this).hide();
               
           };

           var attachVisitedRankData = function() {
               var $this = $(this);
               $this.attr("data-rank", localStorage.getItem($("a:first", $this).attr("href")) || 99999);
           };

           var rankClickedItem = function() {
               var $this = $(this);
               
               $this
                   .parent()
                   .attr("data-rank", 1)
                   .siblings()
                   .each(function(i) {
                             $(this).data("rank", i + 2);
                             localStorage.setItem($("a:first", $(this)).attr("href"), i + 2);
                         });
               localStorage.setItem($this.attr("href"), 1);
               window.location  = $this.attr("href");
           };


           
           var SpotLighter = {};

           SpotLighter.initialize = function(input, output, showAll) {
               var $input = $(input).focus();
               if ($input.length > 0) {
                   var $output = $(output);
                   var $showAll = $(showAll);
                   $showAll.click(_.partial(showAllChildren, $output));
                   $("body")
                       .on("keydown", input, _.partial(interceptActionKeys, $output))
                       .on("keyup", input, _.partial(handleKeyPress, $input, $output, $showAll));
                   $output
                       .on("click", "a", rankClickedItem);
                   $output.children().each(attachVisitedRankData);
                   handleKeyPress($input, $output, $showAll, false);
                   
               }
               

               return this;
           };
           
           return SpotLighter;
           
       });
