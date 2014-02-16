(function() {
  $(function() {
    var $start, tour;
    $start = $("#start");
    tour = new Tour({
      onStart: function() {
        return $start.addClass("disabled", true);
      },
      onEnd: function() {
        location.href='/dash/temas_de_ayuda';
      },
      debug: true
    });
    tour.addSteps([
	{
        element: "#primer-tour",
        placement: "right",
        title: "Detalles del evento",
        content: "Visualiza diferente informacion acerca del evento: descripcion, fecha de inicio/fin, una rapida ubicacion del evento y los usuarios invitados al mismo.",
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
