<template>
    <div>
        <div class="container">
            <navbar></navbar>
            <div class="row row-cols-2">
                <div class="col" v-for="lunchInfo in this.lunchList">
                    <div class="card">
                        <a href="#" class="pop"><img v-bind:src="lunchInfo.imageUrl"
                                                     class="card-img-top lunch-thumbnail"
                                                     v-bind:alt="lunchInfo.name + ' photo'"></a>
                        <div class="card-body">
                            <h5 class="card-title">{{lunchInfo.name}}</h5>
                            <div class="card-text overflow-auto h-25">{{lunchInfo.description}}</div>
                        </div>
                    </div>
                    <br/>
                </div>
            </div>
        </div>
        <div class="modal fade" id="imagemodal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
             aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-body">
                        <button type="button" class="close" data-dismiss="modal"><span
                                aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                        <img src="" class="imagepreview col-sm-12">
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
  import Navbar from './navbar';

  export default {
    components: {Navbar},
    props: {
      lunchClient: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        lunchList: [],
      };
    },
    async created() {
      this.lunchList = await this.lunchClient.fetchLunchesToday();
    },
    updated() {
      $('.pop').on('click', function() {
        $('.imagepreview').attr('src', $(this).find('img').attr('src'));
        $('#imagemodal').modal('show');
      });
    },
  };
</script>

<style scoped>
    .lunch-thumbnail {
        max-height: 200px;
        object-fit: cover;
    }

    .card {
        white-space: pre;
    }
</style>
