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
        element: ".list-content-user-messages",
        placement: "right",
        title: "Mensajes",
        content: "Podras ver si un usuario al que sigues: se hizo fan, ha comentado, o si ha recomendado algun ítem en particular!",
        backdrop: true
      },
      {
        element: ".new-message",
        placement: "right",
        title: "Nuevo mensaje",
        content: "Apretando el botón podrás enviar un mensaje a diferentes usuarios.",
        backdrop: true
      }, {
        element: ".sidebar-stadistic",
        path: "http://www.google.com",
        placement: "left",
        title: "Estadísticas",
        content: "Puedes consultar: la cantidad de ítems de los cuales eres fan, y tambien los usuarios que sigues y te siguen.",
        backdrop: true
      }
    ]);
    tour.start();
    if (tour.ended()) {
      //$('<div class="alert alert-warning"><button class="close" data-dismiss="alert">&times;</button>You ended the demo tour. <a href="#" class="start">Restart the demo tour.</a></div>').prependTo(".content").alert();
    }
    $(document).ready(function() {
      tour.restart();
      return $(".alert").alert("close");
    });
    return $("html").smoothScroll();
  });

}).call(this);
