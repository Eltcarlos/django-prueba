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
</template>

<script>
import backendApi from "../api/backendApi";
import Swal from "sweetalert2";
export default {
  data() {
    return {
      document: {
        nombre: "",
        apellido: "",
        edad: "",
        telefono: "",
        correo: "",
      },
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
  },
};
</script>

<style scoped>
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
</style>
