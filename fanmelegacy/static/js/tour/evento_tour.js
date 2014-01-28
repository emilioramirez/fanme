(function() {
  $(function() {
    var $start, tour;
    $start = $("#start");
    tour = new Tour({
      onStart: function() {
        return $start.addClass("disabled", true);
      },
      onEnd: function() {
        return $start.removeClass("disabled", true);
      },
      debug: true
    });
    tour.addSteps([
	{
        element: "#primer-tour",
        placement: "right",
        title: "Detalles del evento",
        content: "Visualiza diferente informacion acerca del evento: descripcion, fecha de inicio/fin y una rapida ubicacion del evento.",
        backdrop: true
      },{
        element: "#tercer-tour",
        placement: "left",
        title:"Invitados",
        content: "Un listado con los usuarios que han sido invitados al evento.",
        backdrop: true
      }
    ]);
    tour.start();
    if (tour.ended()) {
      //$('<div class="alert alert-warning"><button class="close" data-dismiss="alert">&times;</button>You ended the demo tour. <a href="#" class="start">Restart the demo tour.</a></div>').prependTo(".content").alert();
    }
    $(document).ready(function() {
      tour.restart();
    });
  });

}).call(this);
