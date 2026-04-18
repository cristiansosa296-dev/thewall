// let ipGuardada = "";

// // CONECTAR
// function conectar() {
//     const ip = document.getElementById("ip").value;
//     const estado = document.getElementById("estado");

//     ipGuardada = ip;

//     fetch(`http://${ip}:5000/`)
//         .then(res => res.text())
//         .then(() => {
//             estado.innerText = "🟢 Conectado";
//         })
//         .catch(() => {
//             estado.innerText = "🔴 Error";
//         });
// }
const API = "http://localhost:5000";

async function mover(direccion) {
  await fetch(`${API}/mover/${direccion}`, { method: "POST" });
}

async function detener() {
  await fetch(`${API}/detener`, { method: "POST" });
}

// ========================
// BOTONES (mouse + touch)
// ========================
function bindBoton(id, direccion) {
  const btn = document.getElementById(id);

  // Mouse
  btn.addEventListener("mousedown", () => mover(direccion));
  btn.addEventListener("mouseup", detener);
  btn.addEventListener("mouseleave", detener);

  // Touch (móvil)
  btn.addEventListener("touchstart", (e) => {
    e.preventDefault();
    mover(direccion);
  }, { passive: false });

  btn.addEventListener("touchend", detener);
}

// Asociar botones
bindBoton("btn-w", "adelante");
bindBoton("btn-a", "izquierda");
bindBoton("btn-s", "atras");
bindBoton("btn-d", "derecha");

// ========================
// TECLADO
// ========================
const teclasActivas = new Set();

document.addEventListener("keydown", (e) => {
  const key = e.key.toLowerCase();

  if (teclasActivas.has(key)) return;
  teclasActivas.add(key);

  if (key === "w") mover("adelante");
  if (key === "s") mover("atras");
  if (key === "a") mover("izquierda");
  if (key === "d") mover("derecha");
});

document.addEventListener("keyup", (e) => {
  const key = e.key.toLowerCase();
  teclasActivas.delete(key);

  if (["w", "a", "s", "d"].includes(key)) {
    detener();
  }
});

// ========================
// SEGURIDAD EXTRA
// ========================

// Si cambiás de pestaña → STOP
window.addEventListener("blur", detener);

// Si soltás click fuera → STOP
document.addEventListener("mouseup", detener);

function setearVelocidad(valor) {
  fetch(`${API}/velocidad`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      velocidad: valor
    })
  });
}

// Obtener todos los radios
const radios = document.querySelectorAll('input[name="velocidad"]');

// Escuchar cambios
radios.forEach(radio => {
  radio.addEventListener("change", (e) => {
    if (e.target.checked) {
      setearVelocidad(e.target.value);
    }
  });
});
// document.addEventListener("keyup", (e) => {
//   if (["w", "a", "s", "d"].includes(e.key)) {
//     detener();
//   }
// });
// // MOVER
// function mover(direccion) {

//     let flecha = document.getElementById("flecha");

//     let giro = document.querySelector('input[name="giro"]:checked').value;
//     let velocidad = document.querySelector('input[name="velocidad"]:checked').value;

//     // ADELANTE
//     if (giro === "adelante") {
//         if (direccion === "W") flecha.innerHTML = "⬆";
//         if (direccion === "S") flecha.innerHTML = "⬇";
//         if (direccion === "A") flecha.innerHTML = "↖";
//         if (direccion === "D") flecha.innerHTML = "↗";
//     }

//     // ATRÁS
//     if (giro === "atras") {
//         if (direccion === "W") flecha.innerHTML = "⬆";
//         if (direccion === "S") flecha.innerHTML = "⬇";
//         if (direccion === "A") flecha.innerHTML = "↙";
//         if (direccion === "D") flecha.innerHTML = "↘";
//     }

//     // ENVIAR AL RASPBERRY
//     if (ipGuardada !== "") {
//         fetch(`http://${ipGuardada}:5000/mover?dir=${direccion}&giro=${giro}&vel=${velocidad}`)
//             .then(res => res.text())
//             .then(data => console.log("OK:", data))
//             .catch(err => console.error("Error:", err));
//     }
// }