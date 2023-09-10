$(document).ready(function()
{
   function openSelectInput(selectDiv)
   {
      if( selectDiv.hasClass('hidden') )
      {
         // opening the select
         selectDiv.removeClass('hidden')
         setTimeout(() => {
            selectDiv.toggleClass('-translate-y-5 translate-y-1 opacity-0')
         }, 1)
      } else {
         // closing the select
         selectDiv.toggleClass('opacity-0')
         setTimeout(() => {
            selectDiv.toggleClass('hidden -translate-y-5 translate-y-1')
         }, 300);
      }
   }
   
   $('#main_nav #hamburger_btn').click(function()
   {
      $('#nav_sm').removeClass('hidden')
      $('#nav_sm .dark_bg').toggleClass('opacity-0 opacity-30')
      setTimeout(() => {
         $('#nav_sm #main_menu_navbar').removeClass('-translate-y-full')
      }, 300)
   })

   $('#nav_sm #close_navbar').click(function()
   {
      $('#nav_sm #main_menu_navbar').addClass('-translate-y-full')
      setTimeout(() => {
         $('#nav_sm .dark_bg').toggleClass('opacity-0 opacity-30')
         setTimeout(() => {
            $('#nav_sm').addClass('hidden')
         }, 300)
      }, 400)
   })

   $('#habit_type_input').click(function()
   {
      openSelectInput($('#habit_type_select'))
   })
   
   $('#habit_type_select span').click(function()
   {
      // result change
      let result = $(this).html()
      $('#habit_type_input').html(result)
      $('#habit_type_input').removeClass('text-slate-300')
      $('input#id_habit_type').val(result)

      // closing select
      $('#habit_type_select').toggleClass('opacity-0')
      setTimeout(() => {
         $('#habit_type_select').toggleClass('hidden -translate-y-5 translate-y-1')
      }, 300);
   })

   $('#new_habit_btn').click(function()
   {
      $('#habit_form').toggleClass('hidden flex')
      setTimeout(() => {
         $('#habit_form .dark_bg').toggleClass('opacity-30 opacity-0')
         setTimeout(() => {
            $('#habit_form #form').toggleClass('opacity-0 -translate-y-24')
         }, 150)
      }, 1)
   })

   $('#habit_form .dark_bg').click(function()
   {
      $('#habit_form #form').toggleClass('opacity-0 -translate-y-24')
      setTimeout(() => {
         $('#habit_form .dark_bg').toggleClass('opacity-30 opacity-0')
         setTimeout(() => {
            $('#habit_form').toggleClass('hidden flex')
         }, 200)
      }, 300);
   })

   $('#timeline_input').click(function()
   {
      openSelectInput($('#timeline_select'))
   })




   $('#edit_description_button').click(function()
   {
      $('#description_form').removeClass('hidden')
      $(this).addClass('hidden')
      $('#habit_info p').addClass('hidden')
   })
   $('#description_form button[type=button]').click(function()
   {
      $('#description_form').addClass('hidden')
      $('#edit_description_button').removeClass('hidden')
      $('#habit_info p').removeClass('hidden')
   })


   $('.activate_form').each(function(index)
   {
      index = index
      $(this).click(function()
      {
         $('.activate_form > div').eq(index).toggleClass('-translate-y-[100px]')
         $('.activate_form > p').eq(index).toggleClass('translate-y-[100px]')
      })
   })



   $('#check_flash_wrapper #close_button').click(function()
   {
      $('#main_message').addClass('opacity-0 translate-y-[25px]')
      setTimeout(() => {
         $('#check_flash_wrapper #dark_bg').removeClass('opacity-50')
         setTimeout(() => {
            $('#check_flash_wrapper').toggleClass('flex hidden')
         }, 150)
      }, 350)
   })


   $('#track_wrapper').scroll(function()
   {
      let scroll_position = $(this).scrollLeft()
      let element_width = $(this).prop('scrollWidth') - $(this).width()
      console.log(scroll_position)
      if($('#fade_gradient_left').hasClass('hidden'))
      {
         if(scroll_position > 0) { $('#fade_gradient_left').toggleClass('hidden flex') }
      } else
      {
         if(scroll_position == 0) { $('#fade_gradient_left').toggleClass('hidden flex') }
      }
      if($('#fade_gradient_right').hasClass('hidden'))
      {
         if(scroll_position < element_width - 50) { $('#fade_gradient_right').toggleClass('hidden flex') }
      } else
      {
         if(scroll_position >= element_width - 50) { $('#fade_gradient_right').toggleClass('hidden flex') }
      }
   })

   $('#scroll_helper button[type=button]').click(function()
   {
      let direction = $(this).data('scroll-direction')
      let scroll_size = $('#track_wrapper').width() * (2/3)
      let current_scroll_pos = $('#track_wrapper').scrollLeft()
      let element_width = $('#track_wrapper').prop('scrollWidth') - $('#track_wrapper').width()
      let calculate_scroll_pos = 0

      if(direction == "left")
      {
         calculate_scroll_pos = current_scroll_pos - scroll_size
         if(calculate_scroll_pos <= 0) { calculate_scroll_pos = 0 }
      } else if (direction == "right")
      {
         calculate_scroll_pos = current_scroll_pos + scroll_size
         if(calculate_scroll_pos >= element_width - 50) { calculate_scroll_pos = element_width }
      } else
      {
         (direction == "start") ? calculate_scroll_pos = 0 : calculate_scroll_pos = element_width
      }

      if(calculate_scroll_pos == 0) { $('#fade_gradient_left').toggleClass('hidden flex') }
      if(calculate_scroll_pos == element_width) { $('#fade_gradient_right').toggleClass('hidden flex') }

      
      $('#track_wrapper').scrollLeft(calculate_scroll_pos)
   })



   $('#time_track_form_input').click(function()
   {
      openSelectInput($('#time_track_form_select'))
   })

   $('#time_track_form_select span').click(function()
   {
      // closing select
      $('#time_track_form_select').toggleClass('opacity-0')
      setTimeout(() => {
         $('#time_track_form_select').toggleClass('hidden -translate-y-5 translate-y-1')
      }, 300);

      // change data
      $('#time_track_form_input').html($(this).html())
      $('input[name=level]').val($(this).html())
   })

   $('.add_time_track_button').click(function()
   {
      let date_result = $(this).data('date')
      $('input[name=date_for]').val(date_result)
      $('#add_time_track_form_wrapper').toggleClass('hidden flex')
      setTimeout(() => {
         $('#add_time_track_form_wrapper #dark_bg').toggleClass('opacity-0 opacity-40')
         setTimeout(() => {
            $('#add_time_track_form_wrapper #main_form').toggleClass('opacity-0 scale-[0.85]')
         }, 100)
      }, 1)
   })
   $('#add_time_track_form_wrapper button[type=button]').click(function()
   {
      $('input[name=date_for]').val('date_result')
      $('#add_time_track_form_wrapper #main_form').toggleClass('opacity-0 scale-[0.85]')
      setTimeout(() => {
         $('#add_time_track_form_wrapper #dark_bg').toggleClass('opacity-0 opacity-40')
         setTimeout(() => {
            $('#add_time_track_form_wrapper').toggleClass('hidden flex')
         }, 150)
      }, 200)
   })








   $('.pie_graph_representation').each(function() {
      let neutral_percent = parseInt($(this).data('neutral-percentage'))
      let productive_percent = parseInt($(this).data('productive-percentage'))
      let unproductive_percent = parseInt($(this).data('unproductive-percentage'))
      if( neutral_percent >= 0 )
      {
         unproductive_percent += productive_percent
         $(this).css('background', 'conic-gradient(from 0, #22c55e 0, #22c55e '+ productive_percent +'%, #be123c 0, #be123c '+ unproductive_percent +'%, #0369a1 0, #0369a1 100%)')
      } else
      {
         $(this).css('background', 'conic-gradient(from 0, #22c55e 0, #22c55e '+ productive_percent +'%, #be123c 0, #be123c 100%)')
      }
   })

   $('#show_color_info').click(function()
   {
      let info_div = $('#show_color_info > div')
      if( info_div.hasClass('hidden') )
      {
         info_div.removeClass('hidden')
         setTimeout(() => {
            info_div.toggleClass('opacity-0 scale-90')
         }, 1)
      } else
      {
         info_div.toggleClass('opacity-0 scale-90')
         setTimeout(() => {
            info_div.addClass('hidden')
         }, 300)
      }
   })
})