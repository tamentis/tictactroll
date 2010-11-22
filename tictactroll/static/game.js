/* Constants/Config is on the HTML template. */

/* Where the cursor currently is */
var cursorX = 2;
var cursorY = 2;

/* All the grids in the system. */
var grids = [];

/* Playing... */
var playing = true;
var trolling = true;

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
var p1StatsElement;
var p2StatsElement;
var p1LifeBarElement;
var p2LifeBarElement;
var gameOverModalElement;
var gameOverContainerElement;

/* Timeouts */
var buttonTimeout = null;
var bubbleTimeout = null;

/* Houston says we have no session. */
function handle_no_session() {
  crapOnPlayer("Looks like we lost your session, click on \"Home\" up there.");
}

/* Game is done, timeout, no life, etc... ask the server for the debriefing */
function gameover() {
  playing = false;
  gameOverModalElement.setStyle("display", "block");
  gameOverContainerElement.setStyle("display", "block");
  var xhr = new Request({ url: "/gameover" });
  xhr.onSuccess = function(data) {
    gameOverContainerElement.innerHTML = data;
  };
  xhr.post();
}

/* Refresh the player stats (scores, pieces..) */
function refreshStats(p1, p2) {
  var baseBarWidth = 195.0;

  p1StatsElement.innerHTML = "Valid Crosses: <span style=\"color: #8eb500;\">" +
      p1[1] + "</span><br/>Bad Grids: <span style=\"color: #af091e;\">" +
      p1[2] + "</span>";
  p2StatsElement.innerHTML = "Valid Circles: <span style=\"color: #8eb500;\">" +
      p2[1] + "</span><br/>Bad Grids: <span style=\"color: #af091e;\">NEVAH!" +
      "</span>";

  p1LifeBarElement.setStyle("width", p1[0] + "%");
  p2LifeBarElement.setStyle("width", p2[0] + "%");
}

/* Send a stupid comment to the player */
function crapOnPlayer(msg) {
  var timeout = 2000;

  if (bubbleTimeout)
    clearTimeout(bubbleTimeout);

  if (msg == null) {
    msg = cool_lines.pop();
    if (!msg)
      msg = "Shit, you suck!";
  } else {
    timeout = 5000;
  }

  bubbleContentElement.innerHTML = msg;
  bubbleElement.setStyle("display", "block");
  bubbleTimeout = setTimeout(function() {
    bubbleTimeout = null;
    bubbleElement.setStyle("display", "none");
  }, 2000);
}

/* Position a grid on the board (piece-based coordinates) */
function moveGrid(el, x, y) {
  if (x > (boardSize - 3)) x = boardSize - 3;
  else if (x < 0)          x = 0;
  if (y > (boardSize - 3)) y = boardSize - 3;
  else if (y < 0)          y = 0;
    
  var cursorLeft = x * pieceDist + gridOffset;
  var cursorTop = y * pieceDist + gridOffset;
  el.setStyle("left", cursorLeft + "px");
  el.setStyle("top", cursorTop + "px");

  return [x, y];
}

/* Draw the grid HTML element */
function drawGrid(x, y, color) {
  var el = new Element("div", { "class": "grid-core grid-" + color });
  gridContainerElement.appendChild(el);
  return el;
}

/* Color a set of piece with the given color */
function colorPieces(pieces, color) {
  for (var i = 0; i < pieces.length; i++) {
    var px = pieces[i][0];
    var py = pieces[i][1];
    var pel = $("piece_" + px + "_" + py);
    pel.removeClass("piece-blank");
    pel.addClass("piece-" + color);
  }
}

/* 
 * Player1 has created a new grid, build the element, position it and tell
 * the server about it.
 */
function createGrid(x, y, color) {
  var msg = null;

  var el = drawGrid(x, y, "pending");
  var coords = moveGrid(el, x, y);

  var xhr = new Request.JSON({ url: "/add_grid" });
  xhr.onSuccess = function(data) {
    if (data.status == "much_success") {
      el.removeClass("grid-pending");
      el.addClass("grid-" + color);
      colorPieces(data.pieces, "green");

    } else if (data.status == "overlap") {
      el.removeClass("grid-pending")
      el.addClass("grid-red");
      msg = "Haha... that's overlapping, you suck";

    } else if (data.status == "badspot") {
      el.removeClass("grid-pending")
      el.addClass("grid-red");

    } else if (data.status == "no_session") {
      return handle_no_session()

    } else if (data.status == "gameover") {
      return gameover();

    } else {
      msg = "hmmmm... something went wrong, it's all b0rked =/";
    }

    if (data.p1 || data.p2)
      refreshStats(data.p1, data.p2);

    crapOnPlayer(msg);
  };
  xhr.post({ "x": coords[0], "y": coords[1] });

  grids.push(el);
}

/* Player wants to place a grid, push the button (looks better) and create */
function fire() {
  if (!playing)
    return;

  if (buttonTimeout)
    clearTimeout(buttonTimeout);

  buttonElement.addClass("pressed");
  buttonTimeout = setTimeout(function() {
    buttonTimeout = null;
    buttonElement.removeClass("pressed");
  }, 200);

  createGrid(cursorX, cursorY, "green"); 
}

/* Just find the HTML elements (global vars) */
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
  p1StatsElement = $("player1-stats");
  p2StatsElement = $("player2-stats");
  p1LifeBarElement = $("lifebar1-woot");
  p2LifeBarElement = $("lifebar2-woot");
  gameOverModalElement = $("gameover-modal");
  gameOverContainerElement = $("gameover-container");
}

/*
 * When the document is ready, map all the HTML elements, setup the drag
 * over the board, the events for the button and all the tickers.
 */
document.addEvent("domready", function() {
  mapElements();

  var dragInstance = new Drag(boardElement, {
    "handle": boardGrabberElement
  });

  dragInstance.addEvent("drag", function(el, x1, x2) {
    var offsetLeft = el.offsetLeft;
    var offsetTop = el.offsetTop;
    cursorX = parseInt((offsetLeft * -1 + boardWidth / 2) / pieceDist) - 1;
    cursorY = parseInt((offsetTop * -1 + boardHeight / 2) / pieceDist) - 1;
    moveGrid(cursorElement, cursorX, cursorY);
  });

  buttonElement.addEvent("click", function(event) {
    fire();
  });

  setInterval(function() {
    if (!playing)
      return;

    if (!countDown) {
      dragInstance.stop();
      gameover();
      return;
    }

    countDownElement.innerHTML = --countDown;

    if (trolling) {
      var xhr = new Request.JSON({ url: "/next_troll_grid" });
      xhr.onSuccess = function(data) {
        var msg = null;

        if (data.status == "great_scott") {
          for (var i = 0; i < data.grids.length; i++) {
            var grid = data.grids[i];
            var el = drawGrid(grid[0], grid[1], "pink");
            moveGrid(el, grid[0], grid[1]);
            colorPieces(data.pieces, "pink");
          };

          if (data.p1 || data.p2)
            refreshStats(data.p1, data.p2);

        } else if (data.status == "thats_all_folks") {
          trolling = false;
          return;

        } else if (data.status == "gameover") {
          return gameover();

        } else if (data.status == "no_session") {
          return handle_no_session()

        } else {
          msg = "hmmmm... something went wrong, it's all b0rked =/";
          crapOnPlayer(msg);
        }
      };
      xhr.post();
    }

  }, 1000);
});

document.addEvent("keydown", function(event) {
  if (event.key == "space") {
    fire();
  }
});

