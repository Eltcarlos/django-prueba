<template>
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
import backendApi from "../api/backendApi";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      codigo: "",
      loading: false,
      documento: null,
    };
  },
  methods: {
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
