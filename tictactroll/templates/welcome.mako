## vim:ft=mako encoding=utf-8

<%inherit file="base.mako" />

<%def name="extra_headers()">
  <script type="text/javascript">
    function check() {
      var value = $("username").value;
      if (value.length) {
        return true;
      } else {
        alert("Come one dude, give me a user name, anything!");
        return false;
      }
    }
  </script>
</%def>

<%def name="body()">
  <p style="padding-top: 128px;">
    Welcome to <strong>reddic-tac-troll</strong>! The twisted tic-tac-toe
    where you place the grids, not the shapes. You have ${countdown} seconds
    to place as many grids as you can, they can't overlap and they have to
    contain three crosses aligned. Hit Space or the red button to shoot grids.
  </p>

  <p class="align-center" style="margin-top: 64px;">
    <form action="${request.application_url}/enter_game" onsubmit="return check()">
      <label for="username">Reddit username:&nbsp;</label>
      <input id="username" name="username" />
      <input type="submit" value="Rock on" />
    </form>
  </p>
</%def>
