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
		title: "Logbook",
		content: "Dentro de esta sección podras tener un historial de las actividades de los usuarios que sigues dentro del FanMe!",
		orphan: true
	}, {
        element: "#logbook",
        placement: "right",
        title: "Actividades",
        content: "Podras ver si un usuario al que sigues: se hizo fan, ha comentado, o si ha recomendado algun ítem en particular!",
        backdrop: true
      }, {
        element: ".sidebar-stadistic",
        placement: "left",
        title: "Estadísticas",
        content: "Puedes consultar: la cantidad de ítems de los cuales eres fan, y tambien los usuarios que sigues y te siguen.",
        backdrop: true
      }, {
		element: ".sidebar-menu-indicators",
		placement: "left",
        title: "Movimiento social.",
        content: "Verifica tus actividades sociales con tus seguidores y con los usuarios que sigues.",
        reflex: true,
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
