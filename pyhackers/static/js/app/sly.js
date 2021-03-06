// Generated by CoffeeScript 1.6.3
(function() {
  jQuery(function($) {
    var $items, newItems, next, renderItems, start, template;
    $items = $("#frame");
    template = Handlebars.compile($('#project-template').html());
    start = 0;
    newItems = function(response) {
      start += 50;
      return renderItems(response);
    };
    renderItems = function(response) {
      return $items.append(template({
        projects: response.data,
        start: start
      }));
    };
    next = function() {
      return $.getJSON("/fancy.json?start=" + start, newItems);
    };
    $(document).on("click", "#next", function(evt) {
      next();
      evt.stopPropagation();
      return evt.preventDefault();
    });
    return next();
  });

}).call(this);
