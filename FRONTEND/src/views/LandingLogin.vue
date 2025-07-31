<template>
  <div class="landing">
    <section class="hero">
      <h1>Bienvenido a TaskGamify</h1>
    </section>

    <div class="content-row">
      <section class="description">
        <p>
          ¿Y si las tareas fueran parte de una aventura? <br />
          <br />
          <strong>TaskGamify</strong> transforma el aprendizaje en una
          experiencia divertida y motivadora. Tus alumnos completan tareas,
          ganan monedas virtuales y las canjean por recompensas reales.
        </p>
        <button class="cta">Descubre cómo funciona</button>
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

    <footer class="footer">
      © 2025 TaskGamify. Todos los derechos reservados.
    </footer>
  </div>
</template>
