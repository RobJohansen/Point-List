function a() {
  $(this).parent().find(".grip").toggleClass("fa-chevron-right fa-chevron-down");
}

function b() {
  $(this).toggleClass("fa-bars fa-chevron-right fa-chevron-down");
}

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

  if (t.hasClass("fa-check")) {
    t.toggleClass("fa-check fa-refresh fa-spin");

    var f = p.siblings(".edit").find(".form-inline");

    f.removeClass("has-error");

    if (f.find("input").filter(function() { return this.value == ""; }).length == 0) {
      $.post(
        "/save",
        f.serialize() + "&key=" + p.attr("tag"),
        function () {
          t.toggleClass("fa-pencil fa-check fa-refresh fa-spin");
          p.siblings('.edit').toggle();
          p.siblings('.view').toggle();
        });
    } else {
      f.addClass("has-error");
    }
  } else {
    t.toggleClass('fa-pencil fa-check');
    p.siblings('.edit').toggle();
    p.siblings('.view').toggle();
  }
}

function setup(n) {
  n.find(".fa-plus").click(add);
  n.find(".fa-times").click(remove);
  n.find(".fa-refresh").click(update);
  n.find(".fa-pencil").click(edit);

  n.find(".hide").removeClass("hide").hide();

  n.find(".collapse").on("show.bs.collapse", a);
  n.find(".collapse").on("hide.bs.collapse", a);
  n.find('.grip').hover(b, b);
}

$(document).ready(function() {
  var n = $(this);
  setup(n);
});















// var SPEED = 200;

// function adder() {
//   var t = $(this);

//   $.post("/add", "key=" + t.closest("[tag]").attr("tag"), function(o) {
//     //ROWS
//     var g = $(".header > .group").filter(function() { return this.innerText == o.scheme; });

//     var target = $(g.length == 0 ? ".panel-group" : g.closest(".panel").find('.panel-body').first());

//     var add = $(g.length == 0 ? o.group : o.row);

//     $(add)
//       .hide()
//       .appendTo(target)
//       .slideDown(SPEED, function() {
//         t.remove();

//         t.off("click");

//         add.find(".fa-check").on("click", save);
//         add.find(".fa-pencil").on("click", edit);
//         add.find(".fa-refresh").on("click", updater);
//         add.find(".fa-times").on("click", deleter);

//         add.find(".fa-bars").hide();
//         add.find(".panel-heading").on("mouseover", hover);
//         add.find(".panel-heading").on("mouseout", unhover);

//         $(".panel").removeAttr("style");
        
//         // MENU
//         // if (t.siblings(".group:before").length == 0) t = t.parents(".group:before");
//       });

//   });
// }

// function deleter() {
//   var t = $(this);

//   $.post("/delete", "key=" + t.closest("[tag]").attr("tag"), function(o) {  
//     //ROWS
//     var g = t.closest(".panel");

//     $(g.siblings().length == 0 ? g.parents(".panel") : g)
//       .slideUp(SPEED, function() {
//         g.remove();

//         //MENU
//         var menu = $(".add-menu");
//         var existing = menu.children(".group").filter(function() { return this.innerText == o.group; });

//         var scheme = "<li class='add-option' tag='" + o.id + "'><a href='#'>" + o.name + "</a></li>";
//         var group = "<li class='group'>" + o.group + "</li>";

//         if (existing.length == 0) {
//           // Add Group and Scheme
//           menu.append(group + scheme);
//         } else {
//           // Add Scheme to Group
//           existing.after(scheme);
//         }

//         $("[tag='" + o.id + "'").on("click", adder);
//       });
//   });
// }

// function updater() {
//   var t = $(this);

//   t.addClass("fa-spin");

//   $.get("/update", "key=" + t.closest("[tag]").attr("tag"), function(o) {
//     t.parent().find(".points").html(o.points);
//     t.removeClass("fa-spin");
//   });
// }

// function edit() {
//   var p = $(this).parent();

//   p.siblings(".edit").show();
//   p.hide();
// }

// function save() {
//   var t = $(this);
//   var p = t.parent();

//   p.removeClass("has-error");

//   if (t.siblings().filter(function() { return this.value == ""; }).length == 0) {
    
//     $.post("/save", p.serialize() + "&key=" + p.parent().parent().attr("tag"), function() {
//       p.parent().siblings(".refresh").show();
//       p.parent().hide();
//     });

//   } else {
//     p.addClass("has-error");
//   }
// }

// function hover() {
//   $(this).find(".fa-bars").show();
// }

// function unhover() {
//   $(this).find(".fa-bars").hide();
// }

// $(document).ready(function() {
//   // HIDE
//   $(".hide").removeClass("hide").hide();

//   // SORT
//   $(".sortableItem")
//     .sortable({
//       placeholder : "placeholder",
//       connectWith : ".sortableItem",
//       handle      : ".fa-bars",
//       start       : function(e, ui) {
//                       ui.placeholder.height(ui.item.height());
//                     }
//     })
//     .disableSelection();

//   $(".sortable")
//     .sortable({
//       placeholder : "placeholder",
//       handle      : ".fa-bars",
//       start       : function(e, ui) {
//                       ui.placeholder.height(ui.item.height());
//                     }
//     })
//     .disableSelection();

//   // MOVE
//   $(".fa-bars").hide();

//   $(".panel-heading").hover(hover, unhover);

//   // EDIT
//   $(".fa-pencil").click(edit);

//   $(".fa-check").click(save);



//   $(".fa-refresh").click(updater);
//   $(".fa-times").click(deleter);
//   $(".add-option").click(adder);

// });