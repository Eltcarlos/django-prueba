<template>
  <div class="create-pdf">
    <form class="formulario" @submit.prevent="createDocument">
      <h1 class="formulario__titulo">Crear PDF</h1>
      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="document.nombre" required class="formulario__input" />
      </div>
      <div class="form-group">
        <label for="apellido">Apellido:</label>
        <input type="text" id="apellido" v-model="document.apellido" required class="formulario__input" />
      </div>
      <div class="form-group">
        <label for="edad">Edad:</label>
        <input type="text" id="edad" v-model="document.edad" required class="formulario__input" />
      </div>
      <div class="form-group">
        <label for="telefono">Telefono:</label>
        <input id="telefono" v-model="document.telefono" required class="formulario__input" />
      </div>
      <div class="form-group">
        <label for="correo">Coreo:</label>
        <input type="email" id="correo" v-model="document.correo" class="formulario__input" />
      </div>
      <button type="submit" class="formulario__submit">Crear</button>
    </form>
  </div>

  <div class="search-input">
    <h1>Buscar PDF</h1>
    <div class="search-bar">
      <input type="text" v-model="codigo" placeholder="Ingrese el término de búsqueda" />
      <button @click="getDocument">Buscar</button>
    </div>
    <div class="search-results">
      <h2>Resultados de la búsqueda</h2>
      <div class="card-grid" v-if="documento">
        <button @click="downloadDocument">Descargar</button>
      </div>
      <p v-else>No se encontraron resultados.</p>
    </div>
  </div>
</template>

<script>
import backendApi from "./api/backendApi";
import Swal from "sweetalert2";

export default {
  name: "App",
  components: {},
  data() {
    return {
      document: {
        nombre: "",
        apellido: "",
        edad: "",
        telefono: "",
        correo: "",
      },
      codigo: "",
      loading: false,
      documento: null,
    };
  },
  methods: {
    async createDocument() {
      if (this.validateForm()) {
        try {
          const response = await backendApi.post("/create", this.document);
          if (response.data.success) {
            Swal.fire({
              title: "Creado",
              text: `${response.data.message} su codigo es ${response.data.codigo}`,
              icon: "success",
              confirmButtonText: "Continuar",
            }).then(() => {
              this.document = {
                nombre: "",
                apellido: "",
                edad: "",
                telefono: "",
                correo: "",
              };
            });
          } else {
            Swal.fire({
              title: "Error",
              text: `${response.data.message}`,
              icon: "error",
              confirmButtonText: "Continuar",
            });
          }
        } catch (error) {
          Swal.fire({
            title: "Error",
            text: `${error.response.data.message}`,
            icon: "error",
            confirmButtonText: "Continuar",
          });
        }
      }
    },
    async getDocument() {
      this.documento = null;
      try {
        const response = await backendApi.get(`/document/${this.codigo}`);
        console.log(response);
        if (response.data.success) {
          this.documento = response.data.documento;
        } else {
          Swal.fire({
            title: "Error",
            text: `${response.data.message}`,
            icon: "error",
            confirmButtonText: "Continuar",
          });
        }
      } catch (error) {
        Swal.fire({
          title: "Error",
          text: `${error.response.data.message}`,
          icon: "error",
          confirmButtonText: "Continuar",
        });
      }
    },
    validateForm() {
      // Validar que todos los campos estén completos
      if (
        this.document.nombre &&
        this.document.apellido &&
        this.document.edad &&
        this.document.telefono &&
        this.document.correo
      ) {
        return true;
      } else {
        // Mostrar mensaje de error o realizar alguna acción adicional si algún campo está vacío
        console.error("Por favor complete todos los campos");
        return false;
      }
    },
    downloadDocument() {
      // Descargar el documento
      const link = document.createElement("a");
      link.href = `data:application/pdf;base64,${this.documento}`;
      link.download = `prueba_${this.codigo}.pdf`;
      link.target = "_blank";
      link.click();
      this.documento = null;
      this.codigo = "";
    },
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.create-pdf {
  padding-top: 50px;
}
.formulario {
  padding-top: 20px;
  width: 550px;
  max-width: 100%;
  margin: auto;
  margin-top: 30px;
  padding: 20px;
  box-shadow: 0 0 20px 1px rgba(0, 0, 0, 0.3);
  position: relative;
}
.formulario__titulo {
  text-align: center;
  margin-top: 0;
  color: rgba(0, 0, 0, 0.7);
}
.formulario__input,
.formulario__label,
.formulario__submit {
  display: block;
  width: 90%;
  font-size: 1.3em;
}
.formulario__input {
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.3);
  margin-bottom: 40px;
}
.formulario__input:focus {
  outline: 1px solid rgba(0, 0, 0, 0.7);
}
.formulario__label {
  padding-left: 15px;
  position: absolute;
  margin-top: -85px;
  z-index: -20;
  color: rgba(0, 0, 0, 0.5);
  transition: all 0.2s;
}
.formulario__submit {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  cursor: pointer;
  border: none;
}

.search-input {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.search-bar input {
  padding: 5px;
  font-size: 16px;
}

.search-bar button {
  padding: 5px 10px;
  font-size: 16px;
}

.search-results {
  margin-top: 20px;
}
</style>
