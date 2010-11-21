## vim:ft=mako encoding=utf-8

<%inherit file="base.mako" />

<%def name="extra_headers()">
  <script type="text/javascript" src="${request.application_url}/static/game.js"></script>
  <style type="text/css" media="screen">
    .back-the-fuck-ground {
      background: url(static/back.png);
    }
  </style>
</%def>

<%def name="body()">
  <script type="text/javascript">
    /* Constants/Configuration */
    var boardSize = ${gamestate.board_size};
    var pieceSize = ${gamestate.piece_size};
    var pieceMargin = ${gamestate.piece_margin};
    var pieceDist = ${gamestate.piece_dist};
    var boardWidth = 512;
    var boardHeight = 464;
    var cursorOffset = 9;
    var countDown = ${gamestate.remaining};
  </script>

  <div id="board-container">
    <div id="board">
      <div id="grids">
        <!--div style="left: 84px; top: 84px;" class="grid-core grid-green">&nbsp;</div-->
        <div style="left: 159px; top: 159px;" class="grid-core grid-cursor" id="cursor">&nbsp;</div>
      </div>
      <div id="pieces">
        % for piece in gamestate.pieces: 
          <div style="left: ${piece[0]}px; top: ${piece[1]}px;" class="piece-core piece-blank piece-${piece[2]}">&nbsp;</div>
        % endfor
      </div>
    </div>
  </div>
  <div id="board-grabber">&nbsp;</div>
  <div id="bubble">
    <div id="bubble-content">
      You are such a loser, dude go kill yourself.
    </div>
  </div>
  <div id="lifebar1-back"><div id="lifebar1-woot">&nbsp;</div></div>
  <div id="lifebar2-back"><div id="lifebar2-woot">&nbsp;</div></div>
  <div class="player-image player1-image"><img src="http://en.gravatar.com/avatar/${gamestate.gravatar}?s=160&d=retro" /></div>
  <div class="player-name player1-name">${gamestate.username}</div>
  <div class="player-name player2-name">trollface</div>
  <div id="red-button">&nbsp;</div>
  <div id="count-down">${gamestate.remaining}</div>
</%def>
