<template>
  <div class="landing">
    <section class="hero">
      <h1>Bienvenido a TaskGamify</h1>
    </section>

    <section class="hero-block">
      <div class="content-row">
        <section class="description">
          <p>
            ¿Y si las tareas fueran parte de una aventura? <br />
            <br />
            <strong>TaskGamify</strong> transforma el aprendizaje en una
            experiencia divertida y motivadora. Tus alumnos completan tareas,
            ganan monedas virtuales y las canjean por recompensas reales.
          </p>
          <button class="cta" @click="scrollToHowItWorks">
            Descubre cómo funciona
          </button>
        </section>

        <section class="login">
          <form @submit.prevent="login">
            <h2>Iniciar sesión</h2>
            <input
              v-model="username"
              type="text"
              placeholder="Usuario"
              required
            />
            <input
              v-model="password"
              type="password"
              placeholder="Contraseña"
              required
            />
            <button type="submit">Iniciar sesión</button>
            <p v-if="error" class="error">{{ error }}</p>
          </form>
        </section>
      </div>
    </section>

    <!-- Explicación funcionalidad -->
    <section id="funciona" class="how-it-works">
      <h2>¿Cómo funciona TaskGamify?</h2>
      <div class="steps">
        <div class="step">
          <h3>1. Completa tareas</h3>
          <p>Los profesores asignan tareas que los alumnos deben realizar.</p>
        </div>
        <div class="step">
          <h3>2. Gana monedas</h3>
          <p>Cada tarea validada otorga monedas virtuales al alumno.</p>
        </div>
        <div class="step">
          <h3>3. Canjea recompensas</h3>
          <p>
            Los alumnos utilizan sus monedas para obtener recompensas reales o
            simbólicas.
          </p>
        </div>
      </div>
    </section>

    <footer class="footer">
      © 2025 TaskGamify. Todos los derechos reservados.
    </footer>
  </div>
</template>

<script>
import { useUserStore } from '../stores/userStore';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
    };
  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  methods: {
    async login() {
      try {
        await this.userStore.login(this.username, this.password); // llama al store
        this.error = '';
      } catch (err) {
        this.error = err;
      }
    },
  },
};
</script>

<style scoped>
.landing {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1rem;
  color: white;
  text-align: center;
  min-height: 100vh;
  background: url('/bg.jpg') no-repeat center center fixed;
  background-size: cover;
}

/* Hero */
.hero h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

/* Hero Block */
.hero-block {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.content-row {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
}

/* Description */
.description {
  background-color: rgba(255, 255, 255, 0.9);
  color: #111;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  max-width: 500px;
  width: 100%;
}

.description p {
  margin-bottom: 1rem;
}

.cta {
  background-color: #1e90ff;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 5px;
  cursor: pointer;
}

.cta:hover {
  background-color: #0e70d1;
}

/* Login */
.login {
  background-color: rgba(255, 255, 255, 0.9);
  color: #111;
  padding: 1.5rem;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
}

.login form {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.login input {
  padding: 0.6rem;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.login button {
  padding: 0.6rem;
  background-color: #1e90ff;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: bold;
}

.login button:hover {
  background-color: #0e70d1;
}

.error {
  color: red;
  font-size: 0.9rem;
}

/* Footer */
.footer {
  margin-top: auto;
  padding: 1rem;
  color: white;
  font-size: 0.85rem;
  opacity: 0.9;
}

/* Funcionalidad */
.how-it-works {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  color: #111;
}

.how-it-works h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #ffffff;
}

.steps {
  display: flex;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 4rem 2rem;
  border-radius: 8px;
  gap: 2rem;
}

.step h3 {
  font-size: 1.3rem;
  color: #1e90ff;
  margin-bottom: 0.5rem;
}

.step p {
  font-size: 1rem;
  line-height: 1.5;
}

/* ------------------- RESPONSIVE ------------------- */
@media (min-width: 768px) {
  .landing {
    flex-direction: column;
    justify-content: space-between;
    padding: 4rem 2rem;
    min-height: 100vh;
  }

  .hero-block {
    padding: 4rem 2rem;
    margin-top: -8rem;
  }

  .content-row {
    flex-direction: row;
    justify-content: center;
    gap: 6rem;
  }

  .hero h1 {
    font-size: 3rem;
    margin-bottom: 2rem;
  }

  .landing .content-row {
    display: flex;
    justify-content: center;
    gap: 16rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
  }

  .description,
  .login {
    width: 40%;
    min-width: 350px;
    padding: 2rem;
    font-size: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .description p {
    font-size: 1.1rem;
    line-height: 1.6;
  }

  .cta {
    font-size: 0.95rem;
    padding: 0.8rem 1.5rem;
  }

  .steps {
    flex-direction: row;
    justify-content: center;
    gap: 3rem;
  }

  .step {
    max-width: 300px;
  }

  .footer {
    margin-top: auto;
    padding: 4rem 0;
    font-size: 0.85rem;
    color: #fff;
    text-align: center;
    width: 100%;
    background: transparent;
  }
}
</style>
