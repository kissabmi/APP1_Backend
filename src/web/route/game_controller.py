from flask import Blueprint, jsonify, request


GAME_PAGE = """
<!doctype html>
<html lang='ru'>
<head>
<meta charset='utf-8'>
<title>Крестики-нолики — онлайн</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
  .wrap { max-width: 520px; margin: 0 auto; }
  h1 { text-align: center; color: #333; margin: 0 0 16px; }
  .card { background: #fff; border: 1px solid #ddd; border-radius: 10px;
          padding: 18px; margin: 12px 0; }
  .card h2 { margin: 0 0 12px; font-size: 18px; color: #444; }

  /* форма входа */
  #login input { display: block; width: 100%; padding: 10px; margin: 8px 0;
                 font-size: 15px; border: 1px solid #ccc; border-radius: 6px; }
  #login button { padding: 10px 18px; margin: 6px 4px 0 0; cursor: pointer;
                  border: none; border-radius: 6px; font-size: 14px; }
  .btn-primary { background: #4a7fff; color: #fff; }
  .btn-secondary { background: #e0e0e0; color: #333; }
  #lerr { color: #d33; font-size: 13px; min-height: 18px; margin-top: 6px; }

  /* панель игрока */
  .me { display: flex; justify-content: space-between; align-items: center; }
  .me b { color: #4a7fff; }
  .btn-sm { padding: 4px 12px; font-size: 13px; cursor: pointer;
            border: 1px solid #ccc; border-radius: 4px; background: #fff; }

  /* кнопки создания */
  .actions button { padding: 10px 16px; margin: 4px 4px 4px 0; cursor: pointer;
                    border: none; border-radius: 6px; font-size: 14px; }
  .actions .g { background: #4a7fff; color: #fff; }
  .actions .o { background: #ff9a3c; color: #fff; }
  .actions .r { background: #e0e0e0; color: #333; }

  /* список игр */
  #gamesList { max-height: 160px; overflow-y: auto; }
  .gitem { padding: 10px; border: 1px solid #eee; border-radius: 6px;
           margin: 6px 0; display: flex; justify-content: space-between;
           align-items: center; cursor: pointer; }
  .gitem:hover { background: #f0f4ff; }
  .gitem .gid { font-family: monospace; font-size: 13px; color: #666; }
  .gitem .jbtn { background: #4a7fff; color: #fff; border: none;
                 padding: 6px 14px; border-radius: 4px; cursor: pointer; }
  .empty { color: #999; text-align: center; padding: 16px; }

  /* доска */
  .gameinfo { text-align: center; margin: 8px 0; font-size: 14px; color: #666; }
  .board { display: grid; grid-template-columns: repeat(3, 100px); gap: 6px;
           justify-content: center; margin: 14px auto; }
  .cell { width: 100px; height: 100px; font-size: 42px; cursor: pointer;
          background: #fff; display: flex; align-items: center; justify-content: center;
          border: 2px solid #ccc; border-radius: 8px; user-select: none;
          transition: background 0.15s; }
  .cell:hover { background: #f0f4ff; }
  .cell.x { color: #4a7fff; }
  .cell.o { color: #ff9a3c; }
  .cell.disabled { cursor: not-allowed; opacity: 0.6; }
  .cell.disabled:hover { background: #fff; }
  .status { text-align: center; font-size: 20px; font-weight: bold;
            margin: 12px 0; min-height: 28px; }
  .status.win { color: #2a9d4a; }
  .status.lose { color: #d33; }
  .status.draw { color: #888; }
  .status.turn { color: #4a7fff; }
  .status.wait { color: #ff9a3c; }
  .gidbox { text-align: center; font-size: 12px; color: #999; margin-top: 8px;
            word-break: break-all; }
</style>
</head>
<body>
<div class='wrap'>
<h1>Крестики-нолики</h1>

<!-- ФОРМА ВХОДА -->
<div id='login' class='card'>
  <h2>Вход / Регистрация</h2>
  <input id='lg' placeholder='логин' autocomplete='off'>
  <input id='pw' type='password' placeholder='пароль' autocomplete='off'>
  <div>
    <button class='btn-primary' onclick='doAuth(\"/signup\")'>Регистрация</button>
    <button class='btn-secondary' onclick='doAuth(\"/login\")'>Вход</button>
  </div>
  <p id='lerr'></p>
  <p style='font-size:12px;color:#888;margin-top:10px'>
    Для игры вдвоём открой сайт в двух вкладках/окнах и залогинься разными логинами.
  </p>
</div>

<!-- ИГРА -->
<div id='game' style='display:none'>
  <div class='card me'>
    <span>Ты: <b id='mylogin'>?</b> <span id='myrole' style='font-size:12px'></span></span>
    <button class='btn-sm' onclick='logout()'>Выйти</button>
  </div>

  <div class='card'>
    <h2>Новая игра</h2>
    <div class='actions'>
      <button class='g' onclick='newGame(\"computer\")'>Против компьютера</button>
      <button class='o' onclick='newGame(\"user\")'>Против игрока</button>
      <button class='r' onclick='loadGames()'>Обновить список</button>
    </div>
  </div>

  <div class='card'>
    <h2>Доступные игры (ожидают игрока)</h2>
    <div id='gamesList'><div class='empty'>нет доступных игр</div></div>
  </div>

  <div class='card' id='boardcard' style='display:none'>
    <div class='gameinfo' id='gameinfo'></div>
    <div class='board' id='board'></div>
    <div class='status' id='status'></div>
    <div class='gidbox' id='gidbox'></div>
  </div>
</div>
</div>

<script>
let auth = localStorage.getItem('auth');
let uid  = localStorage.getItem('uid');
let myLogin = '';
let currentGameId = null;
let pollTimer = null;

function setErr(t){ document.getElementById('lerr').textContent = t; }

async function doAuth(ep){
  const lg = document.getElementById('lg').value.trim();
  const pw = document.getElementById('pw').value;
  if(!lg || !pw){ setErr('введи логин и пароль'); return; }
  const b64 = btoa(lg + ':' + pw);
  // регистрация — JSON, вход — сразу Basic auth
  if(ep === '/signup'){
    let r = await fetch('/signup', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({login:lg, password:pw})
    });
    let d = await r.json();
    if(d.error){ setErr(d.error); return; }
  }
  // логин через Basic auth
  let r = await fetch('/login', { method:'POST', headers:{'Authorization':'Basic '+b64} });
  let d = await r.json();
  if(d.error){ setErr(d.error); return; }
  auth = b64; uid = d.user_id;
  localStorage.setItem('auth', auth);
  localStorage.setItem('uid', uid);
  await enterGame();
}

async function enterGame(){
  document.getElementById('login').style.display = 'none';
  document.getElementById('game').style.display = 'block';
  // узнаём свой логин
  const r = await fetch('/user/' + uid, { headers:{'Authorization':'Basic '+auth} });
  const d = await r.json();
  myLogin = d.login || '?';
  document.getElementById('mylogin').textContent = myLogin;
  loadGames();
}

function logout(){
  localStorage.removeItem('auth');
  localStorage.removeItem('uid');
  auth = null; uid = null;
  if(pollTimer){ clearInterval(pollTimer); pollTimer = null; }
  document.getElementById('login').style.display = 'block';
  document.getElementById('game').style.display = 'none';
}

function emptyField(){ return [[0,0,0],[0,0,0],[0,0,0]]; }

async function newGame(opp){
  const r = await fetch('/game/new', {
    method:'POST', headers:{'Authorization':'Basic '+auth,'Content-Type':'application/json'},
    body: JSON.stringify({opponent: opp})
  });
  const d = await r.json();
  if(d.error){ alert(d.error); return; }
  openGame(d.game_id);
}

async function openGame(gid){
  currentGameId = gid;
  document.getElementById('boardcard').style.display = 'block';
  await refreshGame();
  if(pollTimer){ clearInterval(pollTimer); }
  // опрашиваем сервер каждые 2 сек чтобы видеть ход соперника
  pollTimer = setInterval(refreshGame, 2000);
}

async function refreshGame(){
  if(!currentGameId) return;
  const r = await fetch('/game/' + currentGameId, { headers:{'Authorization':'Basic '+auth} });
  const d = await r.json();
  if(d.error){ document.getElementById('status').textContent = d.error; return; }
  renderBoard(d);
}

function amIPlayerX(g){ return g.player_x === uid; }
function amIPlayerO(g){ return g.player_o === uid; }
function myMark(g){ if(amIPlayerX(g)) return 1; if(amIPlayerO(g)) return 2; return 0; }
function markText(v){ return v===1?'X': v===2?'O':''; }

function renderBoard(g){
  const f = g.field;
  const b = document.getElementById('board');
  b.innerHTML = '';
  const mark = myMark(g);
  // можно ли мне ходить
  const myTurn = (g.state==='x_turn' && amIPlayerX(g)) || (g.state==='o_turn' && amIPlayerO(g));
  const gameOver = g.state==='draw' || g.state.startsWith('victory');

  for(let r=0;r<3;r++){
    for(let c=0;c<3;c++){
      const v = f[r][c];
      const d = document.createElement('div');
      d.className = 'cell ' + (v===1?'x': v===2?'o':'');
      d.textContent = markText(v);
      if(myTurn && v===0){
        d.onclick = () => makeMove(r,c);
      } else {
        d.classList.add('disabled');
      }
      b.appendChild(d);
    }
  }

  // роль
  let role = '';
  if(mark===1) role = '(ты X)';
  else if(mark===2) role = '(ты O)';
  else role = '(зритель)';
  document.getElementById('myrole').textContent = role;

  // инфо об игре
  const info = 'Игра: ' + currentGameId.slice(0,8) + '... — X: ' + (g.player_x? g.player_x.slice(0,8):'нет') + ', O: ' + (g.player_o? (g.player_o==='computer'?'комп':g.player_o.slice(0,8)):'нет');
  document.getElementById('gameinfo').textContent = info;
  document.getElementById('gidbox').textContent = 'ID: ' + currentGameId;

  // статус
  const st = document.getElementById('status');
  st.className = 'status';
  if(g.state==='waiting'){
    st.textContent = '⏳ Ожидание второго игрока...';
    st.classList.add('wait');
  } else if(g.state==='draw'){
    st.textContent = '🤝 Ничья!';
    st.classList.add('draw');
  } else if(g.state==='victory_x'){
    st.textContent = mark===1? '🎉 Ты выиграл (X)!' : mark===2? '😢 Ты проиграл (O)' : 'X выиграл';
    st.classList.add(mark===1?'win': mark===2?'lose':'draw');
  } else if(g.state==='victory_o'){
    st.textContent = mark===2? '🎉 Ты выиграл (O)!' : mark===1? '😢 Ты проиграл (X)' : 'O выиграл';
    st.classList.add(mark===2?'win': mark===1?'lose':'draw');
  } else if(g.state==='x_turn'){
    st.textContent = amIPlayerX(g)? '🎯 Твой ход (X)' : '⏳ Ход соперника (X)...';
    st.classList.add('turn');
  } else if(g.state==='o_turn'){
    st.textContent = amIPlayerO(g)? '🎯 Твой ход (O)' : '⏳ Ход соперника (O)...';
    st.classList.add('turn');
  }

  if(gameOver && pollTimer){ clearInterval(pollTimer); pollTimer = null; }
}

async function makeMove(r,c){
  // сначала получаем текущее поле
  const gr = await fetch('/game/' + currentGameId, { headers:{'Authorization':'Basic '+auth} });
  const g = await gr.json();
  if(g.error) return;
  if(g.field[r][c] !== 0) return;
  // ставим свою метку
  const f = g.field.map(row => row.slice());
  const mark = myMark(g);
  f[r][c] = mark;
  const r2 = await fetch('/game/' + currentGameId, {
    method:'POST', headers:{'Authorization':'Basic '+auth,'Content-Type':'application/json'},
    body: JSON.stringify({field: f})
  });
  const d = await r2.json();
  if(d.error){ alert(d.error); return; }
  await refreshGame();
}

async function loadGames(){
  const r = await fetch('/game/available', { headers:{'Authorization':'Basic '+auth} });
  const d = await r.json();
  const list = document.getElementById('gamesList');
  if(d.error){ list.innerHTML = '<div class=\"empty\">'+d.error+'</div>'; return; }
  if(!d.length){ list.innerHTML = '<div class=\"empty\">нет доступных игр — создай новую «Против игрока»</div>'; return; }
  list.innerHTML = '';
  for(const g of d){
    const div = document.createElement('div');
    div.className = 'gitem';
    const isMine = (g.player_x === uid);
    div.innerHTML = '<span class=\"gid\">ID: ' + g.game_id.slice(0,8) + '... (создал: ' + (g.player_x? g.player_x.slice(0,8):'?') + ')</span>';
    if(isMine){
      div.innerHTML += '<span style=\"color:#999;font-size:13px\">твоя — жди</span>';
      div.onclick = () => openGame(g.game_id);
    } else {
      const btn = document.createElement('button');
      btn.className = 'jbtn';
      btn.textContent = 'Присоединиться';
      btn.onclick = (e) => { e.stopPropagation(); joinGame(g.game_id); };
      div.appendChild(btn);
    }
    list.appendChild(div);
  }
}

async function joinGame(gid){
  const r = await fetch('/game/join/' + gid, { method:'POST', headers:{'Authorization':'Basic '+auth} });
  const d = await r.json();
  if(d.error){ alert(d.error); return; }
  openGame(gid);
}

// авто-вход если есть сохранённая сессия
if(auth && uid){
  fetch('/user/' + uid, { headers:{'Authorization':'Basic '+auth} })
    .then(r => r.json())
    .then(d => {
      if(d.error){ logout(); }
      else { enterGame(); }
    })
    .catch(() => logout());
}
</script>
</body>
</html>
"""


def create_game_blueprint(game_service, authenticator):
    game_bp = Blueprint('game', __name__)

    @game_bp.route("/", methods=["GET"])
    def index():
        return GAME_PAGE

    @game_bp.route('/game/new', methods=['POST'])
    @authenticator.authenticate
    def new_game(user_id):
        data = request.get_json()
        if data is None or 'opponent' not in data:
            return jsonify({"error": "opponent required"}), 400

        opponent = data['opponent']
        if not opponent:
            return jsonify({"error": "opponent cannot be empty"}), 400
        game = game_service.create_game(user_id, opponent)

        return jsonify({
            "game_id": game.get_id(),
            "state": game.get_state()
        }), 201

    @game_bp.route('/game/available', methods=['GET'])
    @authenticator.authenticate
    def available_games(user_id):
        games = game_service.get_available_games()
        result = []
        for g in games:
            result.append({
                "game_id": g.get_id(),
                "state": g.get_state(),
                "player_x": g.get_player_x()
            })
        return jsonify(result), 200

    @game_bp.route('/game/join/<game_id>', methods=['POST'])
    @authenticator.authenticate
    def join_game(game_id, user_id):
        game = game_service.join_game(game_id, user_id)
        if game is None:
            return jsonify({"error": "cannot join game"}), 400

        return jsonify({
            "game_id": game.get_id(),
            "state": game.get_state()
        }), 200

    @game_bp.route('/game/<game_id>', methods=['GET'])
    @authenticator.authenticate
    def get_game(game_id, user_id):
        game = game_service.get_game(game_id)
        if game is None:
            return jsonify({"error": "game not found"}), 404

        return jsonify({
            "game_id": game.get_id(),
            "field": game.get_field().get_field(),
            "state": game.get_state(),
            "player_x": game.get_player_x(),
            "player_o": game.get_player_o()
        }), 200

    @game_bp.route('/game/<game_id>', methods=['POST'])
    @authenticator.authenticate
    def make_move(game_id, user_id):
        data = request.get_json()
        if data is None or 'field' not in data:
            return jsonify({"error": "field required"}), 400

        game, error = game_service.make_move(game_id, data['field'], user_id)
        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "game_id": game.get_id(),
            "field": game.get_field().get_field(),
            "state": game.get_state()
        }), 200

    @game_bp.route('/user/<user_id>', methods=['GET'])
    @authenticator.authenticate
    def get_user(user_id, **kwargs):
        from src.domain.service.user_service_impl import UserService
        from src.datasource.repository.user_repository import UserRepository
        user_service = UserService(UserRepository())
        user = user_service.find_by_id(user_id)
        if user is None:
            return jsonify({"error": "user not found"}), 404

        return jsonify({
            "user_id": user.user_id,
            "login": user.login
        }), 200

    return game_bp
