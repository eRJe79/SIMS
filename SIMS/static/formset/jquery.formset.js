$(document).ready(function() {

      // formset control
      $('#addNewRow').on('click', function(e) {
          e.preventDefault();

          var ajax_link = this.getAttribute('data-target-url');

          // +1 to indicate this a request to add new formset instance
          $('#form_with_formset').find('#wtd').val(1);

          $.ajax({
              url: ajax_link,
              data: $('#form_with_formset').serialize(),
              type: 'POST',

              success: function(res) {
                  // clear the formset container and then fill it with the-
                  // response of ajax call. the response contains the-
                  // previous formset instance plus one new instance 
                  $('#formset_container').empty();
                  $('#formset_container').append(res);
              }
          });

          $('#remLastRow').removeAttr('disabled');
      });

      $('#remLastRow').on('click', function(e) {
          e.preventDefault();

          var ajax_link = this.getAttribute('data-target-url');

          // at least one formset instance is mandatory
          if ($('#formset_container').children('table').length > 1) {

              // -1 to indicate this a request to remove the last formset instance
              $('#form_with_formset').find('#wtd').val(-1);

              // because I handled fromsets in separate tables so
              // for remove last instance we just remove the last child (table)
              $('#formset_container table').last().remove();

              $.ajax({
                  url: ajax_link,
                  data: $('#form_with_formset').serialize(),
                  type: 'POST',

                  success: function(res) {
                      $('#formset_container').empty();
                      $('#formset_container').append(res);
                  }
              });
          }
          // disabling remove button if just one instance remained
          if ($('#formset_container').children('table').length <= 1)
              $('#remLastRow').attr('disabled', 'true');
      });
  });

</script>