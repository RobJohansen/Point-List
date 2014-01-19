function add() {
  var t = $(this);
  t.toggleClass("fa-plus fa-refresh fa-spin");

  $.post(
    "/add",
    "key=" + t.closest("[tag]").attr("tag"),
    function(o) {
      var n = $(o.row);

      init(n);
      n.appendTo(".rows");
      order();

      t.toggleClass("fa-plus fa-refresh fa-spin");
    });
}


function remove() {
  var t = $(this);
  t.toggleClass("fa-times fa-refresh fa-spin");

  $.post(
    "/remove",
    "key=" + t.closest("[tag]").attr("tag"),
    function(o) {
      t.closest(".panel").remove();
      t.toggleClass("fa-times fa-refresh fa-spin");
    });
}


function update() {
  var t = $(this);
  t.toggleClass("fa-spin");

  $.get(
    "/update",
    "key=" + t.closest("[tag]").attr("tag"),
    function(o) {
      t.siblings(".points").html(o.points);
      t.closest(".panel").find(".panel-body").html(o.content);
      t.toggleClass("fa-spin");
    });
}


function order() {
  var tags = [];
  $(".rows").find("[tag]").each(function() {
    tags.push($(this).attr("tag"));
  });

  $.post(
    "/order",
    "keys=" + tags,
    function() {
      message("Saved");
    });
}


function edit() {
  var t = $(this);
  var p = t.parent();
  var f = p.siblings(".edit").find(":input");

  if (t.hasClass("fa-check")) {
    t.toggleClass("fa-check fa-refresh fa-spin");
    f.parent().removeClass("has-error");

    if (f.filter(function() { return this.value == ""; }).length == 0) {
      $.post(
        "/save",
        "key=" + t.closest("[tag]").attr("tag") + "&" + f.serialize(),
        function (o) {
          t.closest(".panel-heading").find(".scheme").html(o.name);
          t.toggleClass("fa-pencil fa-check fa-refresh fa-spin");
          p.siblings(".edit").toggle();
          p.siblings(".view").toggle();
        });
    } else {
      t.toggleClass("fa-check fa-refresh fa-spin");
      f.parent().addClass("has-error");
    }
  } else {
    t.toggleClass('fa-pencil fa-check');
    p.siblings(".edit").toggle();
    p.siblings(".view").toggle();
  }
}


function message(m) {
  $(".message")
    .stop(true, true)
    .show()
    .html(m)
    .delay(1000)
    .fadeOut(1000);
}


function a() {
  $(this).parent().find(".btn-grip").toggleClass("fa-chevron-right fa-chevron-down");
}


function b() {
  $(this).toggleClass("fa-bars fa-chevron-right fa-chevron-down");
}


function init(n) {
  n.find(".collapse").on("show.bs.collapse", a);
  n.find(".collapse").on("hide.bs.collapse", a);

  n.find(".btn-grip").hover(b, b);
  n.find(".btn-add").click(add);
  n.find(".btn-remove").click(remove);
  n.find(".btn-update").click(update);
  n.find(".btn-edit").click(edit);

  n.find(".hide").removeClass("hide").hide();
}


$(document).ready(function() {
  init($(this));

  $(".message").hide();

  $(".rows")
    .sortable({
      placeholder : "placeholder",
      handle      : ".btn-grip",
      start       : function(e, ui) {
                      ui.placeholder.height(ui.item.height());
                  },
      stop        : function(e, ui) {
                      order();
                  }
    })
    .disableSelection();
});