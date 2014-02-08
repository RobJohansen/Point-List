function add() {
  add_generic($(this), 'add');
}

function add_group() {
  add_generic($(this), 'add_group');
}

function add_generic(t, url) {
  t.toggleClass('fa-plus fa-refresh fa-spin');

  $.post(
    url,
    'key=' + t.closest('[tag]').attr('tag'),
    function(o) {
      var n = $(o.node);

      hookup(n);
      n.appendTo('.main > .rows');
      order();                                                                                                  //TODO - Remove From Add Menu

      t.toggleClass('fa-plus fa-refresh fa-spin');
    });
}


function remove() {
  var t = $(this);
  var p = t.parent();
  var f = p.siblings('.edit').find(':input');

  if (p.siblings('.edit').is(':visible')) {
    f.parent().removeClass('has-error');

    f.each(function() {
      $(this).val($(this).attr('value'));
    });
    p.siblings('.edit').toggle();
    p.siblings('.view').toggle();
    t.siblings('.fa').toggleClass('fa-check fa-pencil');
  } else {
    bootbox.confirm("Are you sure you want to delete this?", function(confirmed) {
      if (confirmed) {
        t.toggleClass('fa-refresh fa-spin');
        
        $.post(
          '/remove',
          'key=' + t.closest('[tag]').attr('tag'),
          function(o) {
            var p = t.closest('.panel');
            p.find('.row').each(function() {
              $(this).appendTo('.main > .rows');
            });
            p.remove();                                                                                                  //TODO - Add To Add Menu
            
            t.toggleClass('fa-refresh fa-spin');
            order();
          });
      }
    });
  }
}


function enter(e) {
  if (e.which == 13) {
    submit($(this).closest('.panel-heading').find('.btn-edit'));
  }
}


function edit() {
  var t = $(this);
  var f = t.parent().siblings('.edit').find(':input');

  if (t.hasClass('fa-check')) {
    submit(t);
  } else {
    t.toggleClass('fa-pencil fa-check');
    t.parent().siblings('.edit').toggle();
    t.parent().siblings('.view').toggle();
    //f.first().focus();                                                                                        //TODO - Fix Toggling
    //f.first().val(f.first().val());
  }
}


function submit(t) {
  var f = t.parent().siblings('.edit').find(':input');

  t.toggleClass('fa-check fa-refresh fa-spin');

  f.parent().removeClass('has-error');

  if (f.filter(function() { return this.value == ''; }).length == 0) {
    $.post(
      '/save',
      'key=' + t.closest('[tag]').attr('tag') + '&' + f.serialize(),
      function (o) {
        f.each(function() {
          $(this).attr('value', $(this).val());
        });
        t.parent().siblings('.edit').toggle();
        t.parent().siblings('.view').toggle();
        t.toggleClass('fa-pencil fa-check fa-refresh fa-spin');

        t.closest('.panel-heading').find('.scheme').html(o.name);
      });
  } else {
    t.toggleClass('fa-check fa-refresh fa-spin');
    f.parent().addClass('has-error');
  }
}


function update() {
  var t = $(this);
  t.toggleClass('fa-spin');

  t.siblings('.error').html('');

  $.get(
    '/update',
    'key=' + t.closest('[tag]').attr('tag'),
    function(o) {
      if (o.success == true) {
        var b = t.closest('.panel').find('.panel-body');
        
        b.html(o.content);
        b.show();
        b.parent().collapse('show');

        t.siblings('.points').html(o.points);
      } else {
        t.siblings('.error').html('ERROR');
      }
      
      t.toggleClass('fa-spin');
    });
}


function order() {
  var tags = [];
  $('.main > .rows > * > [tag]').each(function() {
    var t = $(this);
    if (!t.parent().hasClass('row')) {
      var subtags = []

      t.parent().find('[tag]').each(function() {
        subtags.push($(this).attr('tag'));
      });

      tags.push(subtags);
    }
    tags.push(t.attr('tag'));
  });

  $.post(
    '/order',
    'keys=' + JSON.stringify(tags),
    function() {
      $('.message')
        .stop(true, true)
        .show()
        .delay(3000)
        .fadeOut(1000);
    });
}


function a() {
  $(this).parent().find('.btn-grip').first().toggleClass('fa-chevron-right fa-chevron-down');                 //TODO - Don't modify Parents
}


function b() {
  $(this).toggleClass('fa-bars fa-chevron-right fa-chevron-down');
}


function hookup(t) {
  t.find('.collapse').on('show.bs.collapse', a);
  t.find('.collapse').on('hide.bs.collapse', a);

  t.find('.btn-grip').hover(b, b);

  t.find('.btn-remove').click(remove);
  t.find('.btn-update').click(update);
  t.find('.btn-edit').click(edit);

  t.find('.hide').removeClass('hide').hide();

  t.find(':input').keypress(enter);

  t.find('.rows')
    .sortable({
      placeholder : 'placeholder',
      handle      : '.btn-grip',
      connectWith : '.rows',
      revert      : true,
      start       : function(e, ui) {
                      ui.placeholder.height(ui.item.height());
                    },
      stop        : function(e, ui) {
                      order();
                    },
      receive     : function(e, ui) {
                      if (ui.item.hasClass('group')) $(ui.sender).sortable('cancel');                           //TODO - Recursive Nesting
                    }
    })
    .disableSelection();
}


$(document).ready(function() {
  $('.btn-add').click(add);
  $('.btn-add-group').click(add_group);

  hookup($(this));
});