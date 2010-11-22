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
    var gridOffset = ${gamestate.grid_offset};
    var countDown = ${gamestate.remaining};
    var cool_lines = ${gamestate.cool_lines_as_json()};

  </script>

  <div id="board-container">
    <div id="board">
      <div id="grids">
        % for grid in gamestate.grids:
          <div style="left: ${grid.board_x}px; top: ${grid.board_y}px;" class="grid-core grid-${grid.color}">&nbsp;</div>
        % endfor
        <div style="left: 159px; top: 159px;" class="grid-core grid-cursor" id="cursor">&nbsp;</div>
      </div>
      <div id="pieces">
        % for piece in gamestate.pieces.itervalues(): 
          <div id="piece_${piece.x}_${piece.y}" style="left: ${piece.board_x}px; top: ${piece.board_y}px;" class="piece-core piece-${piece.color} piece-${piece.shape}">&nbsp;</div>
        % endfor
      </div>
    </div>
  </div>
  <div id="board-grabber">&nbsp;</div>
  <div id="gameover-modal">&nbsp;</div>
  <div id="gameover-container">
  </div>
  <div id="bubble">
    <div id="bubble-content">
      You are such a loser, dude go kill yourself.
    </div>
  </div>
  <div id="lifebar1-back"><div id="lifebar1-woot" style="width: ${gamestate.get_p1_stats()[0]}%;">&nbsp;</div></div>
  <div id="lifebar2-back"><div id="lifebar2-woot" style="width: ${gamestate.get_p1_stats()[0]}%;">&nbsp;</div></div>
  <div class="player-image player1-image"><img src="http://en.gravatar.com/avatar/${gamestate.gravatar}?s=160&d=retro" /></div>
  <div class="player-name player1-name">${gamestate.username}</div>
  <div class="player-name player2-name">CPU McTrollface</div>
  <div id="player1-stats" class="player-stats player1-stats">
    Valid Crosses: <span style="color: #8eb500;">${gamestate.get_p1_stats()[1]}</span><br/>
    Bad Grids: <span style="color: #af091e;">${gamestate.get_p1_stats()[2]}</span>
  </div>
  <div id="player2-stats" class="player-stats player2-stats">
    Valid Circles: <span style="color: #8eb500;">${gamestate.get_p1_stats()[1]}</span><br/>
    Bad Grids: <span style="color: #af091e;">NEVAH!</span>
  </div>
  <div id="red-button">&nbsp;</div>
  <div id="count-down">${gamestate.remaining}</div>
</%def>
