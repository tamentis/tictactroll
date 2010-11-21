/* Constants/Config is on the HTML template. */

/* Where the cursor currently is */
var cursorX = 3;
var cursorY = 3;

/* All the grids in the system. */
var grids = [];

/* HTML Element */
var boardElement;
var boardContainerElement;
var boardGrabberElement;
var buttonElement;
var gridContainerElement;
var cursorElement;
var bubbleElement;
var bubbleContentElement;
var countDownElement;

/* Timeouts */
var buttonTimeout = null;
var bubbleTimeout = null;


function crapOnPlayer(msg) {
  if (bubbleTimeout)
    clearTimeout(bubbleTimeout);

  if (msg == null) {
    msg = "Get the fuck out!";
  }

  bubbleContentElement.innerHTML = msg;
  bubbleElement.setStyle("display", "block");
  bubbleTimeout = setTimeout(function() {
    bubbleTimeout = null;
    bubbleElement.setStyle("display", "none");
  }, 2000);
}

function moveGrid(el, x, y) {
  if (x > (boardSize - 2)) x = boardSize - 2;
  else if (x < 1)          x = 1;
  if (y > (boardSize - 2)) y = boardSize - 2;
  else if (y < 1)          y = 1;
    
  var cursorLeft = (x - 1) * pieceDist + cursorOffset;
  var cursorTop = (y - 1) * pieceDist + cursorOffset;
  el.setStyle("left", cursorLeft + "px");
  el.setStyle("top", cursorTop + "px");
}

function createGrid(x, y, color) {
  var msg = null;
  var el = new Element("div", { "class": "grid-core grid-pending" });
  moveGrid(el, x, y);
  gridContainerElement.appendChild(el);

  var xhr = new Request.JSON({ url: "/add_grid" });
  xhr.onSuccess = function(data) {
    if (data.status == "much_success") {
      el.removeClass("grid-pending");
      el.addClass("grid-" + color);

    } else if (data.status == "overlap") {
      el.removeClass("grid-pending")
      el.addClass("grid-red");

    } else if (data.status == "badspot") {
      el.removeClass("grid-pending")
      el.addClass("grid-red");

    } else {
      msg = "hmmmm... something went wrong, it's all b0rked =/";
    }

    crapOnPlayer(msg);
  };
  xhr.post({ "x": 1, "y": 2 });

  grids.push(el);
}

function fire() {
  if (buttonTimeout)
    clearTimeout(buttonTimeout);

  buttonElement.addClass("pressed");
  buttonTimeout = setTimeout(function() {
    buttonTimeout = null;
    buttonElement.removeClass("pressed");
  }, 200);

  createGrid(cursorX, cursorY, "green"); 
}

function mapElements() {
  boardElement = $("board");
  boardContainerElement = $("board-container");
  boardGrabberElement = $("board-grabber");
  buttonElement = $("red-button");
  gridContainerElement = $("grids");
  cursorElement = $("cursor");
  bubbleElement = $("bubble");
  bubbleContentElement = $("bubble-content");
  countDownElement = $("count-down");
}

document.addEvent("domready", function() {
  mapElements();

  var dragInstance = new Drag(boardElement, {
    "handle": boardGrabberElement
  });

  dragInstance.addEvent("drag", function(el, x1, x2) {
    var offsetLeft = el.offsetLeft;
    var offsetTop = el.offsetTop;
    cursorX = parseInt((offsetLeft * -1 + boardWidth / 2) / pieceDist);
    cursorY = parseInt((offsetTop * -1 + boardHeight / 2) / pieceDist);
    moveGrid(cursorElement, cursorX, cursorY);
  });

  buttonElement.addEvent("click", function(event) {
    fire();
  });

  setInterval(function() {
    if (countDown)
      countDownElement.innerHTML = --countDown;
  }, 1000);
});

document.addEvent("keydown", function(event) {
  if (event.key == "space") {
    fire();
  }
});

