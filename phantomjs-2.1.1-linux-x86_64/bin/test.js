var webPage = require('webpage');
var page = webPage.create();

page.open('https://tocapp.surge.sh/', function(status) {

  var title = page.evaluate(function() {
    return document.getElementsByTagName("button")[0].click()
  });

  console.log(title);
  phantom.exit();

});
