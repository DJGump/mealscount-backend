<template>
  <section class="state-detail my-3" v-if="district != null">
    <div class="container">
      <div class="row" v-if="district.code != 'new'">
        <div class="col-sm">
          <router-link
            :to="{name:'state-detail', params: {state:state_code} }"
          >&laquo; Back to state</router-link>
        </div>
      </div>

      <div class="row">
        <h1 class="col-sm-12">
          <span v-if="editMode"><input v-model="district.name" ></span><span v-else>{{ district.name }} </span>
            ( <span v-if="editMode"><input v-model="district.code"></span><span v-else>{{ district.code }}</span>
             - {{ state_code }})
          </h1>
      </div>

      <DistrictSummary 
        v-bind:district="district" 
        v-bind:schoolDays="schoolDays" 
        v-bind:editMode="editMode" 
      />

      <!-- <ScenarioControl /> -->
    </div>

    <div class="container">
      <div class="row">
        <div class="col-sm alert alert-warning" role="alert">
          <strong>⚠️ PLEASE NOTE</strong>
          <p>The data shown for this district is from the publicly available <a href="https://frac.org/research/resource-library/community-eligibility-cep-database" target="_blank">2019-2020 FRAC CEP database</a> 

          <p>Sites listed may include charter schools and exclude some preschool/early learning programs under your jurisdiction.</p>

          <p>To get the best recommended grouping, you should edit the school list as well as data affiliated with each school to better reflect current enrollment, eligibility, and meal participation.</p> 

          <p>For more information, please <router-link to="/contact">Contact Us</router-link>!</p>

        </div>
      </div>
    </div>

    <div class="container" v-if="district != null && viewMode == 'group'">
        <DistrictGroupView v-bind:district="district" />
    </div>

    <div class="container-fluid">
      <div v-if="district != null && viewMode == 'table'" class="row buttons">
          <div class="col-sm-6">
                <button
                  v-if="!editMode"
                  v-bind:class="{ 'btn-secondary': editMode, 'btn-primary': !editMode }"
                  class="btn"
                  type="button"
                  data-toggle="button"
                  aria-pressed="false"
                  autocomplete="off"
                  v-on:click="toggleEdit"
                >Edit</button>

                <button
                  v-if="edited && editMode"
                  class="btn btn-primary"
                  type="button"
                  data-toggle="button"
                  aria-pressed="true"
                  autocomplete="off"
                  v-on:click="submit"
                >Submit</button>

                <span class="optimize_badge badge badge-secondary" v-if="'optimization_info'in district">Optimized on {{ district.optimization_info.timestamp }} in {{ district.optimization_info.time.toFixed(2) }}s</span>
                <span v-if="edited" class="badge badge-primary" >edited</span>

          </div>
          <div class="col-sm-6 text-right">
            <!--
                <button
                  class="btn btn-primary"
                  type="button"
                  data-toggle="button"
                  aria-pressed="true"
                  autocomplete="off"
                  v-on:click="openScenarioModal"
                >Load / Save Scenario</button>
            -->
                <button
                  class="btn btn-primary"
                  type="button"
                  data-toggle="button"
                  aria-pressed="true"
                  autocomplete="off"
                  v-on:click="export_to_csv"
                >Export to CSV</button>

                <button
                  class="btn btn-primary"
                  type="button"
                  data-toggle="button"
                  aria-pressed="true"
                  autocomplete="off"
                  v-on:click="import_from_file"
                >Import from File</button>

                <button
                  class="btn btn-primary"
                  type="button"
                  data-toggle="button"
                  aria-pressed="true"
                  autocomplete="off"
                  v-on:click="reload"
                >Reload Original</button>

               <a href="#" @click="openFirstTimeModal">help</a>
          </div>
      </div>
      <div class="row px-1">
          <DistrictSchoolView 
            class="col-sm-12" 
            v-bind:schools="district.schools" 
            v-bind:best_group_index="best_group_index" 
            v-bind:reimbursement_index="reimbursement_index" 
            v-bind:editMode="editMode" 
            @toggleEdit="toggleEdit" 
            @recalculate="recalculate"
            />
      </div>
      <div class="row">
        <div class="col-sm">
          <sup>1</sup>
          Based on {{ schoolDays }} days in school year
          <br />
          <sup>2</sup> Pre-loaded data is derived from publicly available FRAC CEP Database.
          <br />
          </div>
      </div>

    </div>  
    <div class="overlay">
      Please wait, optimization is running...
    </div>
    <LoadingModal v-if="showLoading" />
    <ExportModal v-if="showExport" v-bind:district="district" @close="closeExportModal" v-bind:grouping_index="best_group_index" v-bind:reimbursement_index="reimbursement_index" />
    <ImportModal v-if="showImport" v-bind:district="district" @close="closeImportModal"  />
    <ScenarioModal v-if="showScenarioModal" v-bind:district="district" @close="closeScenarioModal" />
    <DistrictDetailFirstTimeModal v-if="showFirstTimeModal" v-bind:district="district" @close="closeFirstTimeModal" />
  </section>
</template>

<script>
import * as _ from "lodash";
import DistrictSummary from "./DistrictSummary.vue"
import ScenarioModal from "./ScenarioModal.vue"
import DistrictSchoolView from "./DistrictSchoolView.vue"
import DistrictGroupView from "./DistrictGroupView.vue"
import ExportModal from "./ExportModal.vue"
import ImportModal from "./ImportModal.vue"
import LoadingModal from "./LoadingModal.vue"
import DistrictDetailFirstTimeModal from "./DistrictDetailFirstTimeModal.vue"

// TODO "404" if no district?
// TODO break this down into little components...
export default {
  components: {
    DistrictSummary,
    ScenarioModal,
    DistrictSchoolView,
    ExportModal,
    DistrictDetailFirstTimeModal,
    ImportModal,
    LoadingModal,
  },
  props: ["state_code", "district_code"],
  data() {
    return {
      editMode: false,
      edited: false,
      viewMode: "table", // or "group"
      schoolDays: 180,
      showExport: false,
      showScenarioModal: false,
      showFirstTimeModal: false,
      showImport: false,
      showLoading: false,
    }
  },
  mounted(){
    if( window.localStorage == undefined || window.localStorage.getItem("mc-district-detail-firsttime") == null ){
      this.showFirstTimeModal = true;
      if(window.localStorage){ window.localStorage.setItem("mc-district-detail-firsttime","done") }
    }
    if(typeof olark !== 'undefined'){
      olark('api.box.show');
    }
  },
   computed: {
    district() {
      return this.$store.getters.selected_district;
    },
    grouped_schools() {
      if (this.district == null || this.district == null) {
        return [];
      }
      const s = this.district.strategies[this.district.best_index];
      const grouped = [];
      const schools = this.district.schools;
      var i = 1;
      s.groups.forEach(g => {
        const group = {
          id: i,
          data: g,
          schools: _.filter(schools, s => {
            return g.school_codes.indexOf(s.school_code) >= 0;
          })
        };
        i++;
        grouped.push(group);
      });
      return _.orderBy( grouped, ['data.isp'], 'desc');
    },
    best_strategy() {
      if (this.district == null || this.district == null) {
        return null;
      }
      if (!this.district.strategies) {
        return null;
      }
      return this.district.strategies[this.district.best_index];
    },
    best_group_index() {
      if (this.best_strategy == null) {
        return {};
      }
      const group_index = {};
      var i = 1;
      this.best_strategy.groups.forEach(g => {
        g.school_codes.forEach(sc => {
          group_index[sc] = i;
        });
        i += 1;
      });
      return group_index;
    },
    reimbursement_index(){
      if (this.best_strategy == null) {
        return {};
      }
      const rt_index = {};
      this.best_strategy.groups.forEach(g => {
        if(g.school_reimbursements){
          g.school_reimbursements.forEach(sc => {
            rt_index[sc[0]] = sc[1] * this.schoolDays;
          });
        }
      });
      return rt_index;
    }
  },
  watch: {
    district(){
      this.showLoading = false;
    }
  },
  methods: {
    toggleEdit() {
      this.editMode = !this.editMode;
      this.edited = true
    },
    submit(){
      console.log("Submitting for optimization",this.district) 
      const null_adp = this.district.schools.filter( s => {
        return (s.daily_breakfast_served == null ||  s.daily_lunch_served == null)
      })
      if(null_adp.length > 0){
        alert("Please fill in all breakfast and lunch daily participation")
        return false;
      }
      this.editMode = false
      this.$store.dispatch("run_district",this.district);
      this.showLoading = true
    },
    recalculate(){
      this.$store.dispatch("calculate_district",this.district);
      this.showLoading = true
    },
    reload(){
      this.$store.dispatch("load_district",{code:this.district.code,state:this.district.state_code});
      this.edited = false
    },
    save_scenario(){
      // todo pop up scenario modal
    },
    export_to_csv(){
      // todo figure out how to export to CSV
      this.showExport = true;
    },
    import_from_file(){
      this.showImport = true; 
    },
    daily_reimbursement_by_school ( school_code ){
      if(this.district_form.reimbursement_rates == null){
        return "";
      }
      return "?"

      // TODO - how do we determine group rate for this school?
      // if group ISP < 0.4, $0
      // if group ISP < 0.625, paid rate
      // else free rate
      const s = this.school_form[school_code];
      const v = ( s.daily_breakfast_served * this.district_form.reimbursement_rates.free_bfast ) 
                 + ( s.daily_lunch_served * this.district_form.reimbursement_rates.free_lunch )
      return v;
    },
    closeExportModal(){
      this.showExport = false;
    },
    closeImportModal(){
      this.showImport = false;
    },
    closeScenarioModal(){
      this.showScenarioModal = false;
    },
    openScenarioModal(){
      this.showScenarioModal = true;
    },
    closeFirstTimeModal(){
      this.showFirstTimeModal = false;
    },
    openFirstTimeModal(){
      this.showFirstTimeModal = true;
    },
  },
};
</script>

<style scoped>
tr.inactive {
  font-style: italic;
  color: #999;
}
input {
  width: 4em;
}

tr.add_row {
  background-color: #eee;
}
tr.add_row td input {
  width: 100%;
}
.optimize_badge {
  animation: fadeInAnimation ease 1s;
  animation-iteration-count: 1; 
  animation-fill-mode: forwards; 
} 
  
@keyframes fadeInAnimation { 
    0% { opacity: 0; } 
    100% { opacity: 1; } 
} 

.buttons button {
  margin: 8px;
}

table.school-table {
  font-size: 10pt;
}
</style>