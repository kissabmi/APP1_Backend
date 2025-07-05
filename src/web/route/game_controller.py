from flask import Blueprint, jsonify, request


GAME_PAGE = """
<!doctype html>
<html lang='ru'>
<head>
<meta charset='utf-8'>
<title>Крестики-нолики</title>
<style>
  body { font-family: sans-serif; text-align: center; margin: 20px; background: #fafafa; }
  h1 { margin-bottom: 6px; }
  #login { max-width: 320px; margin: 30px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #fff; }
  #login input { display: block; width: 90%; margin: 8px auto; padding: 8px; font-size: 14px; }
  #login button { margin: 8px 4px 0; padding: 8px 16px; cursor: pointer; }
  #game { display: none; }
  .panel { margin: 16px auto; padding: 12px; max-width: 480px; border: 1px solid #ddd; border-radius: 8px; background: #fff; }
  .panel button { padding: 6px 14px; margin: 4px; cursor: pointer; }
  .board { display: grid; grid-template-columns: repeat(3, 90px); gap: 4px; justify-content: center; margin: 12px auto; }
  .cell { width: 90px; height: 90px; font-size: 36px; cursor: pointer; background: #f0f0f0;
          display: flex; align-items: center; justify-content: center; border: 1px solid #bbb; border-radius: 4px; }
  .cell:hover { background: #e0e0e0; }
  .status { font-size: 16px; margin: 8px; min-height: 24px; font-weight: bold; }
  #gamesList { text-align: left; max-height: 120px; overflow-y: auto; }
  #gamesList div { padding: 4px 8px; border-bottom: 1px solid #eee; cursor: pointer; }
  #gamesList div:hover { background: #f0f0f0; }
</style>
</head>
<body>
<h1>Крестики-нолики</h1>

<div id='login'>
  <h2>Вход</h2>
  <input id='lg' placeholder='логин' autocomplete='off'>
  <input id='pw' type='password' placeholder='пароль' autocomplete='off'>
  <button onclick='doLogin()'>Войти</button>
  <button onclick='doSignup()'>Регистрация</button>
  <p id='lerr' style='color:red;font-size:13px;min-height:18px'></p>
</div>

<div id='game'>
  <div class='panel'>
    <button onclick='newGame("computer")'>Игра vs комп</button>
    <button onclick='newGame("user")'>Игра vs игрок</button>
    <button onclick='loadGames()'>Обновить список</button>
  </div>
  <div class='panel'>
    <b>Доступные игры:</b>
    <div id='gamesList'></div>
  </div>
  <div class='panel'>
    <div class='board' id='board'></div>
    <div class='status' id='status'></div>
    <div id='gid' style='font-size:13px;color:#666'></div>
  </div>
  <button onclick='logout()'>Выйти</button>
</div>

<script>
let auth = localStorage.getItem('auth');
let uid = localStorage.getItem('uid');
let currentGame = null;

const LINES = [[0,0,0,1,0,2],[1,0,1,1,1,2],[2,0,2,1,2,2],
               [0,0,1,0,2,0],[0,1,1,1,2,1],[0,2,1,2,2,2],
               [0,0,1,1,2,2],[0,2,1,1,2,0]];

function setErr(t){ document.getElementById('lerr').textContent = t; }

async function doSignup(){ await authReq('/signup'); }
async function doLogin(){ await authReq('/login'); }

async function authReq(ep){
  const lg = document.getElementById('lg').value.trim();
  const pw = document.getElementById('pw').value;
  if(!lg || !pw){ setErr('введи логин и пароль'); return; }
  const resp = await fetch(ep, {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({login:lg, password:pw})
  });
  const data = await resp.json();
  if(data.error){ setErr(data.error); return; }
  // login for basic auth
  const b64 = btoa(lg + ':' + pw);
  const lr = await fetch('/login', { method:'POST', headers:{'Authorization':'Basic '+b64} });
  const ld = await lr.json();
  if(ld.error){ setErr(ld.error); return; }
  auth = b64; uid = ld.user_id;
  localStorage.setItem('auth', auth);
  localStorage.setItem('uid', uid);
  showGame();
}

function showGame(){
  document.getElementById('login').style.display = 'none';
  document.getElementById('game').style.display = 'block';
  renderBoard();
  loadGames();
}

function logout(){
  localStorage.removeItem('auth');
  localStorage.removeItem('uid');
  auth = null; uid = null;
  document.getElementById('login').style.display = 'block';
  document.getElementById('game').style.display = 'none';
}

function emptyField(){ return [[0,0,0],[0,0,0],[0,0,0]]; }

function renderBoard(){
  const f = currentGame ? currentGame.field : emptyField();
  const b = document.getElementById('board');
  b.innerHTML = '';
  for(let r=0;r<3;r++){
    for(let c=0;c<3;c++){
      const d = document.createElement('div');
      d.className = 'cell';
      d.textContent = f[r][c] === 1 ? 'X' : f[r][c] === 2 ? 'O' : '';
      d.onclick = () => move(r,c);
      b.appendChild(d);
    }
  }
  const st = document.getElementById('status');
  const gid = document.getElementById('gid');
  if(currentGame){
    gid.textContent = 'Игра: ' + currentGame.game_id;
    st.textContent = stateText(currentGame.state);
  } else {
    gid.textContent = '';
    st.textContent = 'Создай новую игру';
  }
}

function stateText(s){
  if(s === 'x_turn') return 'Ход X';
  if(s === 'o_turn') return 'Ход O';
  if(s === 'draw') return 'Ничья';
  if(s === 'victory_x') return 'X выиграл!';
  if(s === 'victory_o') return 'O выиграл!';
  if(s === 'waiting') return 'Ожидание игрока';
  return s;
}

async function newGame(opp){
  const resp = await fetch('/game/new', {
    method:'POST', headers:{'Authorization':'Basic '+auth,'Content-Type':'application/json'},
    body: JSON.stringify({opponent: opp})
  });
  const data = await resp.json();
  if(data.error){ document.getElementById('status').textContent = data.error; return; }
  currentGame = {game_id: data.game_id, field: emptyField(), state: data.state};
  renderBoard();
}

async function move(r,c){
  if(!currentGame) return;
  if(currentGame.state !== 'x_turn') return;
  const f = currentGame.field.map(row => row.slice());
  if(f[r][c] !== 0) return;
  f[r][c] = 1;
  const resp = await fetch('/game/' + currentGame.game_id, {
    method:'POST', headers:{'Authorization':'Basic '+auth,'Content-Type':'application/json'},
    body: JSON.stringify({field: f})
  });
  const data = await resp.json();
  if(data.error){ document.getElementById('status').textContent = data.error; return; }
  currentGame.field = data.field;
  currentGame.state = data.state;
  renderBoard();
}

async function loadGames(){
  const resp = await fetch('/game/available', { headers:{'Authorization':'Basic '+auth} });
  const data = await resp.json();
  const list = document.getElementById('gamesList');
  if(data.error){ list.innerHTML = data.error; return; }
  if(!data.length){ list.innerHTML = '<div style="color:#999">нет доступных игр</div>'; return; }
  list.innerHTML = '';
  for(const g of data){
    const d = document.createElement('div');
    d.textContent = g.game_id.slice(0,8) + '... (X: ' + (g.player_x||'?').slice(0,8) + ')';
    d.onclick = () => joinGame(g.game_id);
    list.appendChild(d);
  }
}

async function joinGame(gid){
  const resp = await fetch('/game/join/' + gid, { method:'POST', headers:{'Authorization':'Basic '+auth} });
  const data = await resp.json();
  if(data.error){ document.getElementById('status').textContent = data.error; return; }
  currentGame = {game_id: data.game_id, field: emptyField(), state: data.state};
  renderBoard();
}

if(auth && uid){ showGame(); }
</script>
</body>
</html>
"""


def create_game_blueprint(game_service, authenticator):
    game_bp = Blueprint('game', __name__)

    @game_bp.route("/", methods=["GET"])
    def index():
        return GAME_PAGE

    return game_bp
