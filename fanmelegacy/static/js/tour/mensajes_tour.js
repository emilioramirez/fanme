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
        element: "#content-messages",
        placement: "right",
        title: "Mensajes",
        content: "Consulta los mensajes que otros usuarios te han mandado.",
        backdrop: true
      }, {
        element: "#new-message",
        placement: "right",
        title: "Nuevo mensaje",
        content: "Apretando el botón podrás enviar un mensaje a diferentes usuarios.",
        backdrop: true
      }, {
        element: ".sidebar-stadistic",
        path: "http://127.0.0.1:8000/social/messages_user_ayuda/"
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
