<template>
  <div class="home">
    <div id="banner" role="img" aria-label="Fondo lluvioso">
      <div class="container py-5">
        <p class="text-md-center fs-4 m-2 fw-bold">
          LA PLATA
        </p>
        <h1>GESTIÓN DE INUNDACIONES</h1>
        <p class="m-2">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam, esse. Reprehenderit eum aliquam similique. Velit
          ipsa dolore eaque reiciendis, illo officiis cum eveniet ratione veritatis, nemo, iusto perferendis dolor atque!
        </p>
        <a href="#"  class="btn btn-primary px-4">Conocer más</a>
      </div>
    </div>
    <section class="py-4 container">
    <div class="row ">
        <div class="col-lg-3 my-2 ">
          <div class="card h-100 cardS1" data-aos="zoom-in">
            <div class="card-body">
              <h5 class="card-title h5">REALIZAR <span class="d-block">DENUNCIA</span></h5>
              <p class="card-text">
                Lorem ipsum dolor sit amet consectetur, adipisicing elit. Consectetur, doloribus numquam saepe deleniti eos explicabo omnis incidunt nihil non, quidem soluta. Eos provident doloremque deserunt, aperiam sed eum placeat architecto.
              </p>
            </div>
            <div class="card-footer">
              <router-link class="btn btn-outline-primary cardS1" to="/realizar_denuncia">Consultar</router-link> 
            </div>
          </div>
        </div>
        <div class="col-lg-3 my-2 ">
          <div class="card h-100 cardS2" data-aos="zoom-in">
            <div class="card-body">
              <h5 class="card-title h5">PUNTO DE <span class="d-block">ENCUENTRO</span></h5>
              <p class="card-text">
                Lorem ipsum dolor, sit amet consectetur adipisicing elit. Voluptatibus laudantium nisi accusamus. Eos adipisci vel expedita quidem libero praesentium quae corrupti ratione numquam quos est dolore fuga eum, debitis molestias!
              </p>
            </div>
            <div class="card-footer">
              <router-link class="btn btn-outline-primary cardS2" to="/gestion_evacuacion">Consultar</router-link> 
            </div>
          </div>
        </div>
        <div class="col-lg-3 my-2 ">
          <div class="card h-100 cardS2" data-aos="zoom-in">
            <div class="card-body ">
              <h5 class="card-title h5">RECORRIDOS DE <span class="d-block">EVACUACIÓN</span></h5>
              <p class="card-text">
                Lorem ipsum dolor sit, amet consectetur adipisicing elit. Non voluptatibus sit quam optio, reiciendis sint ipsam animi consequatur veniam numquam eius nisi ullam delectus autem itaque iure recusandae, fuga iusto?
              </p>
              
            </div>
            <div class="card-footer">
              <router-link class="btn btn-outline-primary cardS2" to="/gestion_evacuacion">Consultar</router-link> 
            </div>
          </div>
        </div>
        <div class="col-lg-3 my-2 ">
          <div class="card h-100 cardS2" data-aos="zoom-in">
            <div class="card-body">
              <h5 class="card-title h5">ZONAS <span class="d-block">INUNDABLES</span></h5>
              <p class="card-text">
                Lorem ipsum dolor sit amet consectetur, adipisicing elit. Asperiores vitae odio doloremque deserunt voluptate neque? Consectetur aliquam 
              </p>
            </div>
            <div class="card-footer">
              <router-link class="btn btn-outline-primary cardS2" to="/zonas_inundables">Consultar</router-link> 
            </div>
          </div>
        </div>
      
      </div>
    </section>
  </div>

</template>

