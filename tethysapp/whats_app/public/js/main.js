var map = L.map('map').setView([-23.533773, -46.625290], 12);

L.esri.basemapLayer('Topographic').addTo(map);

$('#whats-app-request').click(function(){
          let date = $("#whats-app-date").val();
          let type = $('input[name="search-i"]:checked').val();
          let search = $("#search").val();
          $.ajax({
                   type: "GET",
                   url: window.location.origin +"/apps/whats-app/search",
                   dataType: "json",
                   data: {"date": date, "s_type": type, "search": search},
                   success: function(response) {
                      var parse = JSON.parse(response.message);
                      $.each(parse, function(index, obj) {
                          let coordinates = obj.lat.toString() +',' + obj.longit.toString()
                          let location = coordinates.split(',').map(Number)
                          let serialize = obj.media.split(",")
                          let images = ""
                          $.each(serialize, function(i,image){
                            i_class = "map-image"
                            if (i == 0) {
                              i_class = "first-map-image"
                            } 
                            images += '<a target="_blank" href="/static/whats_app/images/'+image+'"><img class="'+i_class +'" src="/static/whats_app/images/'+image+'"/></a>'
                            console.log(images)
                          })
                          L.marker(location).addTo(map)
                          .bindPopup('<div class="pop-images">'+images+'</div><p><strong>Title:</strong> '+obj.title+'</p><p><strong>Submitter:</strong> '+obj.name+'</p><p><strong>Description:</strong> '+obj.desc+'</p>')
                          .openPopup();
                    
                      })
                   
                   },
                   error: function(rs, e) {
                      alert(rs.responseText);
                    }
              }); 

        })

$(function() {
  var start = moment().subtract(29, 'days');
  var end = moment();
  function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

  $('input[name="daterange"]').daterangepicker({
    startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);
   cb(start, end);
});

