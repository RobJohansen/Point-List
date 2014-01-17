function add() {
  var t = $(this);
  t.toggleClass("fa-plus fa-refresh fa-spin");

  $.post(
    "/add",
    "key=" + t.closest("[tag]").attr("tag"),
    function(o) {
      var n = $(o.row);
      setup(n);

      n.appendTo(".rows");

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


function edit() {
  var t = $(this);
  var p = t.parent();
  var f = p.siblings(".edit").find(".form-inline");

  if (t.hasClass("fa-check")) {
    t.toggleClass("fa-check fa-refresh fa-spin");
    f.removeClass("has-error");

    if (f.find("input").filter(function() { return this.value == ""; }).length == 0) {
      $.post(
        "/save",
        f.serialize() + "&key=" + p.attr("tag"),
        function () {
          t.toggleClass("fa-pencil fa-check fa-refresh fa-spin");
          p.siblings(".edit").toggle();
          p.siblings(".view").toggle();
        });
    } else {
      t.toggleClass("fa-check fa-refresh fa-spin");
      f.addClass("has-error");
    }
  } else {
    t.toggleClass('fa-pencil fa-check');
    p.siblings(".edit").toggle();
    p.siblings(".view").toggle();
  }
}


function a() {
  $(this).parent().find(".btn-grip").toggleClass("fa-chevron-right fa-chevron-down");
}


function b() {
  $(this).toggleClass("fa-bars fa-chevron-right fa-chevron-down");
}


function setup(n) {
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
  setup($(this));

  $(".rows")
    .sortable({
      placeholder : "placeholder",
      handle      : ".btn-grip",
      start       : function(e, ui) {
                      ui.placeholder.height(ui.item.height());
                    }
    })
    .disableSelection();
});