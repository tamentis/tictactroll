## vim:ft=mako encoding=utf-8

<%inherit file="base.mako" />


<%def name="body()">
  <h1 style="padding-top: 64px;">So what's cool about tic-tac-troll</h1>

  <p>
    It's using the latest framework from the Pylons team. Mostly because I
    needed an excuse to play with it =)
  </p>

  <p>
    The concept is different (pretty unique as far as I can tell, with my
    weak google-fu).
  </p>

  <p>
    It has a cool and responsive UI, even though it was not really part of
    the challenge.
  </p>

  <p>
    The entire game state is held by the server so you can refresh at any
    point.
  </p>

  <p>
    The comments of the CPU (Trollface) are coming from reddit, I scan the
    few first articles of wtf and get a few relevant comments to have the
    bot talk a little while you play. It's a python script run by cron which
    never does more than one request every two seconds.
  </p>

  <p>
    Except for the red button and trollface SVG, everything else was done
    with Inkscape and the Gimp.
  </p>

  <h1 style="padding-top: 32px;">Okay.. what's not so cool</h1>

  <p>
    Well since I'm discovering Pyramid, my database access is done directly
    from my gamestate class. Not perfect, it could be decoupled better, if the
    model gets bigger I would use SQLAlchemy.
  </p>

  <p>
    The JS could be encapsulated better.
  </p>
</%def>
