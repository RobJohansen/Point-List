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


function update() {
  var t = $(this);
  t.toggleClass("fa-spin");

  $.get(
    "/update",
    "key=" + t.closest("[tag]").attr("tag"),
    function(o) {
      if (o.success == true) {
        var b = t.closest(".panel").find(".panel-body");
        
        b.html(o.content);
        b.show();
        b.parent().collapse('show');                                      //TIDY

        t.siblings(".points").html(o.points);
      } else {
        alert('error');
      }
      
      t.toggleClass("fa-spin");
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
          f.each(function() {
            $(this).attr("value", $(this).val());
          });
          p.siblings(".edit").toggle();
          p.siblings(".view").toggle();
          t.toggleClass("fa-pencil fa-check fa-refresh fa-spin");
          t.closest(".panel-heading").find(".scheme").html(o.name);
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


function remove() {
  var t = $(this);
  var p = t.parent();
  var f = p.siblings(".edit").find(":input");

  if (p.siblings(".edit").is(":visible")) {
    f.parent().removeClass("has-error");

    f.each(function() {
      $(this).val($(this).attr("value"));
    });
    p.siblings(".edit").toggle();
    p.siblings(".view").toggle();
    t.siblings(".fa").toggleClass("fa-check fa-pencil");
  } else {
    t.toggleClass("fa-refresh fa-spin");
    $.post(
      "/remove",
      "key=" + t.closest("[tag]").attr("tag"),
      function(o) {
        t.closest(".panel").remove();
        t.toggleClass("fa-refresh fa-spin");
        order();
      });
  }
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
      $(".message")
        .stop(true, true)
        .show()
        .delay(3000)
        .fadeOut(1000);
    });
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