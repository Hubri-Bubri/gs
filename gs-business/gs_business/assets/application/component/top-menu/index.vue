<template>
        <div>
  <b-navbar type="dark" variant="primary" toggleable>
    <b-navbar-toggle target="nav_dropdown_collapse"></b-navbar-toggle>
    <b-collapse is-nav id="nav_dropdown_collapse">
      <b-navbar-nav>
      
        <!-- Navbar dropdowns -->
        <b-nav-item-dropdown text="Projekte">
          <b-dropdown-item to="/info" href="#">Projekte (HelloWorld)</b-dropdown-item>
          <b-dropdown-item to="/">Angebote (Root)</b-dropdown-item>
          <b-dropdown-item href="#">Aufträge</b-dropdown-item>
          <b-dropdown-item href="#">Rechnungen</b-dropdown-item>
          <b-dropdown-item href="#">OP-Ausgleich</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Auftragsübersicht">
          <b-dropdown-item href="#">T-Verlauf</b-dropdown-item>
          <b-dropdown-item href="#">Schadenberichte</b-dropdown-item>
          <b-dropdown-item href="#">Leckageberichte</b-dropdown-item>
          <b-dropdown-item href="#">Gerätenliste</b-dropdown-item>
          <b-dropdown-item href="#">Gerätenlager</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="SUB-Unternehmer">
          <b-dropdown-item href="#">SUB-Daten</b-dropdown-item>
          <b-dropdown-item href="#">SUB-Aufträge</b-dropdown-item>
          <b-dropdown-item href="#">E-Rechnungen</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Stammdaten">
          <b-dropdown-item href="#">Kundendaten</b-dropdown-item>
          <b-dropdown-item href="#">Anspechpartner</b-dropdown-item>
          <b-dropdown-item href="#">Versicherungen</b-dropdown-item>
          <b-dropdown-item href="#">Sachverständige</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Statistiken">
          <b-dropdown-item href="#">Monatsumsatz</b-dropdown-item>
          <b-dropdown-item href="#">Kundenumsatz</b-dropdown-item>
          <b-dropdown-item href="#">Partnerumsatz</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Einstellungen">
          <b-dropdown-item href="#">Mitarbeiter</b-dropdown-item>
          <b-dropdown-item href="#">Einstellungen</b-dropdown-item>
          <b-dropdown-item href="#">Einheiten</b-dropdown-item>
          <b-dropdown-item href="#">Fuhrpark</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>

</div>
</template>


<script type="text/javascript">
const items = [
  { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
]
    export default {
         data () {
            return {
              items: items
            }
          }
    }
</script>
