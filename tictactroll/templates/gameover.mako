## vim:ft=mako

<h1>Game Over!</h1>
<table class="pts-table">
  <tr>
    <th>Crosses:&nbsp;</th>
    <td>${stats[1]} x 1,000&nbsp;=&nbsp;</td>
    <td>${fmt(stats[1] * 1000)} pts</td>
  </tr>
  <tr>
    <th>Bad Grids:&nbsp;</th>
    <td>${stats[2]} x -1,000&nbsp;=&nbsp;</td>
    <td>${fmt(stats[2] * -1000)} pts</td>
  </tr>
  <tr>
    <th>Life Left:&nbsp;</th>
    <td>${int(stats[0])}% x 200&nbsp;=&nbsp;</td>
    <td>${fmt(int(stats[0]) * 200)} pts</td>
  </tr>
  <tr>
    <th>Total:&nbsp;</th>
    <td></td>
    <th>${fmt(stats[1] * 1000 + stats[2] * -1000 + int(stats[0]) * 200)} pts</th>
  </tr>
</table>

<h1>High Scores</h1>
<table class="pts-table">
  % for name, score in gamestate.get_hiscores():
    <tr><th>${name}&nbsp;</th><td style="text-align: left;">${fmt(score)} pts</td></tr>
  % endfor
</table>
