## vim:ft=mako encoding=utf-8

<%inherit file="base.mako" />

<%def name="body()">
  <p style="padding-top: 128px;">
    Welcome to <strong>reddic-tac-troll</strong>! The twisted tic-tac-toe
    where you place the grids, not the shapes. You have ${countdown} seconds
    to place as many grids as you can, they can't overlap and they have to
    contain three crosses aligned. Hit Space or the red button to shoot grids.
  </p>

  <p class="align-center" style="margin-top: 64px;">
    <form action="${request.application_url}/enter_game">
      <label for="username">Reddit username:&nbsp;</label>
      <input name="username" />
      <input type="submit" value="Rock on" />
    </form>
  </p>
</%def>
