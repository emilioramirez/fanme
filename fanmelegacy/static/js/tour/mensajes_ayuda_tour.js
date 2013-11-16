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
        element: "#messages",
        placement: "right",
        title: "Mensajes",
        content: "Podras ver todos los mensajes que has enviado con otro usuario en forma de conversación.",
        backdrop: true
      }, {
        element: "#responder",
        placement: "right",
        title: "Responder",
        content: "Podrás usar este campo de texto para responder el mensaje.",
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
