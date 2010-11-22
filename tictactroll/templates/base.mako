## vim:ft=mako encoding=utf-8
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">

<%def name="extra_headers()"></%def>

<head>
	<title>tictactroll</title>
	<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
	<meta name="keywords" content="tictactoe tic tac toe troll reddit" />
	<meta name="description" content="tic tac troll web gane" />
	<link rel="shortcut icon" href="${request.application_url}/static/favicon.ico" />
	<link rel="stylesheet" href="${request.application_url}/static/pylons.css" type="text/css" media="screen" charset="utf-8" />
	<link rel="stylesheet" href="${request.application_url}/static/screen.css" type="text/css" media="screen" charset="utf-8" />
	<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Nobile:regular,italic,bold,bolditalic&amp;subset=latin" type="text/css" media="screen" charset="utf-8" />
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/mootools/1.3.0/mootools-yui-compressed.js"></script>
  <script type="text/javascript" src="${request.application_url}/static/mootools-more.js"></script>
  ${self.extra_headers()}
	<!--[if !IE 7]>
	<style type="text/css">
		#wrap {display:table;height:100%}
	</style>
	<![endif]-->
</head>

<body>
	<div id="wrap">
		<div id="header">
			<div class="header">Le reddic-tac-troll &middot; [
        <a href="/">home</a> &middot;
        <a href="/new_game">new game</a> &middot;
        <a href="/about">about</a>
      ]</div>
		</div>

    <div class="align-center">
      <div class="back-the-fuck-ground">
        <div class="stuff">
          ${self.body()}
        </div>
      </div>
    </div>
	</div>
	<div id="footer">
		<div class="footer">
      © Copywrong 2010, <a href="http://tamentis.com/">tamentis</a> &middot;
      powered by <a href="http://docs.pylonshq.com/pyramid/dev/">Pyramid</a></div>
	</div>
</body>

</html>
