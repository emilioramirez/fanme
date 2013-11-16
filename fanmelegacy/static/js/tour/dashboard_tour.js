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
		title: "Dashboard",
		content: "Dentro de esta sección podras ver todas las recomendaciones que FanMe ha encontrado para ti!",
		orphan: true
	}, {
        element: "#filter-content",
        placement: "right",
        title: "Filtros",
        content: "Podras filtrar los items recomendados según el Tópico que quieras ver!",
        backdrop: true
      }, {
        element: "#recomendaciones-content",
        title: "Recomendaciones",
        content: "Podras visualizar los items recomendados por FanMe.",
        backdrop: true
      }, {
        element: "#item-botones",
        placement: "left",
        title: "Acciones",
        content: "Podras hacerte Fan de un Item o recomendar a una persona que te siga",
        backdrop: true
      }, {
        element: ".sidebar-stadistic",
        placement: "left",
        title: "Estadisticas",
        content: "Visualiza tu participacion en FanMe.",
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
