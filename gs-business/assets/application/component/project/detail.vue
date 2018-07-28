<template>
    <container>
        <b-modal
        size="lg"
        centered
        ok-only
        id="map"
        title="Track">
            <b-embed
            type="iframe"
            aspect="16by9"
            :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+project.street">
            </b-embed>
        </b-modal>
        <b-form
        @submit="offerOk"> 
            <b-modal
            size="md"
            centered 
            hide-header-close
            id="addOffer"
            title="Add Offer">
                <b-form-group
                horizontal
                :label-cols="4"
                label="Order Number:"
                label-for="OrderNumber"
                style="padding: 5px;">
                    <b-form-input 
                    v-model="project.number"
                    class="cForm-input"
                    id="OrderNumber"
                    disabled
                    :state="null"
                    type="text"
                    placeholder="Enter number" />  
                </b-form-group>
                <b-form-group
                horizontal
                :label-cols="4"
                label="Type Of Work:"
                label-for="work"
                style="padding: 5px;">
                    <b-form-select
                    class="select"
                    id="work"
                    :options="works"
                    v-model="add_offer.work"
                    required />
                </b-form-group>
                <b-form-group
                horizontal
                :label-cols="4"
                label="Insurance Number:"
                label-for="InsuranceNumber"
                style="padding: 5px;padding-top: 8px;">
                    <b-form-input
                    class="cForm-input"
                    id="InsuranceNumber"
                    :state="null"
                    type="number"
                    v-model="add_offer.insurance_number"
                    placeholder="Enter number"
                    required />
                </b-form-group>                         
                <b-form-group
                horizontal
                :label-cols="4"
                label="Place:"
                label-for="place"
                style="padding: 5px;">
                    <b-form-input
                    class="cForm-input" 
                    id="place"
                    placeholder="Enter place"
                    :rows="2"
                    :max-rows="4"
                    required
                    v-model="add_offer.place" />
                </b-form-group>               
                <b-form-textarea
                class="cForm-text"
                id="textarea1"
                placeholder="Enter something"
                :rows="2"
                :max-rows="6"
                required
                v-model="add_offer.comment" />
                <template
                slot="modal-footer">
                    <b-button
                    type="submit"
                    variant="primary">
                        OK
                    </b-button>
                </template>
            </b-modal>
        </b-form>
        <container-header
        class="container-fluid">
            <top-menu>
            </top-menu>
        </container-header>
        <container-body class="container-fluid">
            <b-card-group deck>
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Project">
                            <container>
                                <container-body>
                                    <b-container fluid>
                                        <b-row>
                                            <b-col sm="6" class="cuestomRow">
                                                <b-form-group
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Project Number:"
                                                label-for="project-number">
                                                    <b-form-input
                                                    id="project-number"
                                                    :state="null"
                                                    disabled
                                                    type="text"
                                                    v-model="project.number"
                                                    placeholder="Enter project number"
                                                    class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Date:"
                                                label-for="date">
                                                    <b-form-input
                                                    id="date"
                                                    :state="null"
                                                    type="date"
                                                    v-model="project.date"
                                                    placeholder="Enter date"
                                                    class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Editor:"
                                                label-for="editor">
                                                    <b-form-input
                                                    id="editor"
                                                    :state="null"
                                                    type="text"
                                                    v-model="project.editor"
                                                    placeholder="Enter editor name"
                                                    class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
                                            <b-col
                                            sm="6"
                                            class="cuestomRow">
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Street:"
                                                label-for="street">
                                                    <b-input-group>
                                                        <b-form-input
                                                        id="street"
                                                        :state="null"
                                                        type="text"
                                                        v-model="project.street"
                                                        placeholder="Enter street"
                                                        class="cForm-inputBeforG" />
                                                        <b-button
                                                        v-b-modal.map
                                                        class="cForm-inputG">
                                                          G
                                                        </b-button>
                                                    </b-input-group>
                                                </b-form-group>   
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="City:"
                                                label-for="city">
                                                    <b-form-input
                                                    id="city"
                                                    :state="null"
                                                    type="text"
                                                    v-model="project.city"
                                                    placeholder="Enter city"
                                                    class="cForm-input" />
                                                </b-form-group>   
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Zip code:"
                                                label-for="zip-code">
                                                    <b-form-input
                                                    id="zip-code"
                                                    :state="null"
                                                    type="text"
                                                    v-model="project.zip"
                                                    placeholder="Enter zip code"
                                                    class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
                                        </b-row>
                                        <hr />
                                        <b-row> 
                                            <b-col
                                            sm="6"
                                            class="cuestomRow">
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Customer:"
                                                label-for="customer">
                                                    <v-select taggable label="name" v-model="customer" :options="area" />
                                                </b-form-group> 
                                                <b-form-group
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Contact person:"
                                                label-for="contact-person"
                                                v-if="availablePersons">
                                                    <v-select taggable v-model="person" :options="availablePersons" />
                                                </b-form-group> 
                                            </b-col>
                                            <b-col
                                            sm="6"
                                            class="cuestomRow">
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="E-mail:"
                                                v-if="person" >
                                                    <b-button
                                                    class="customButton"
                                                    :href="'mailto:'+person.mail">
                                                        {{person.mail}}
                                                    </b-button>
                                                </b-form-group> 
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Phone:"
                                                v-if="person">
                                                    <b-button
                                                    class="customButton"
                                                    :href="'cal:'+person.tel">
                                                        {{person.tel}}
                                                    </b-button>
                                                </b-form-group> 
                                                <b-form-group 
                                                horizontal
                                                :label-cols="4"
                                                class="cForm"
                                                label="Fax:"
                                                v-if="person">
                                                    <b-button
                                                    class="customButton"
                                                    :href="'cal:'+person.fax">
                                                        {{person.fax}}
                                                    </b-button>
                                                </b-form-group>
                                            </b-col>
                                        </b-row>
                                        <hr />
                                        <b-row>
                                            <b-col>
                                                <b-button
                                                class="customButton"
                                                v-b-modal.addOffer> <!--@click.prevent="newTab"-->
                                                    Add Offer
                                                </b-button>   
                                                <b-button
                                                class="customButton">
                                                    Add Assignment
                                                </b-button> 
                                                <b-button
                                                class="customButton">
                                                    Add Invoice
                                                </b-button>
                                            </b-col>   
                                        </b-row>
                                    </b-container>   
                                    <b-table striped hover :items="items" />
                                </container-body>
                            </container>
                        </b-tab>
                        <b-tab
                        title="Price List"
                        style="padding:0px;">
                            <b-container
                            class="warpTree">
                                <transition
                                name="slide">
                                    <b-col
                                    cols="2"
                                    class="navigation navTree"
                                    style="padding:0px;border-right: 1px solid #dee2e6;" 
                                    id="mySidenav"
                                    v-show="show"
                                    @mouseleave="mouseOut">
                                        <div
                                        class="navigation navTree" >
                                            <div
                                            class="navigation-filter"
                                            align="center"
                                            style=" padding-top: 10px;">
                                                <input
                                                type="text"
                                                class="filter-input"
                                                v-model="treeFilter"
                                                placeholder="Type to filter...">
                                            </div>
                                            <div
                                            class="navigation-tree">
                                                <tree
                                                :data="treeData"
                                                :options="treeOptions"
                                                :filter="treeFilter"
                                                v-model="selectedNode">
                                                    <div
                                                    class="tree-scope"
                                                    slot-scope="{ node }">
                                                        <template
                                                        v-if="node.data.isRoot">
                                                            <span
                                                            class="text"
                                                            style="font-size:14px">
                                                                {{ node.text }}
                                                            </span>
                                                        </template>
                                                        <template
                                                        v-else>
                                                            <span
                                                            class="text">
                                                                {{ node.text }}
                                                            </span>
                                                        </template>
                                                    </div>
                                                </tree>
                                            </div>
                                        </div>
                                    </b-col>
                                </transition>
                                <b-row
                                style="height:100%;">
                                    <div @click="tmouseOver"
                                    style="height:100%;cursor:pointer;background-color:#f7f7f7;padding:5px;display:flex;align-items:center;border-right:1px solid #dee2e6;">
                                        <i class="fas fa-angle-right" />
                                    </div>
                                    <b-col
                                    class="contentTree"
                                    style="padding-top:8px;">
                                        <div>
                                            <div
                                            v-if="!selectedNode || selectedNode.hasChildren()">
                                                Select the menu item
                                            </div>
                                            <b-table
                                            v-else
                                            :items="selectedNode.data.content"
                                            :fields="fieldsPrice" 
                                            class="tableProject"
                                            small>
                                                <template
                                                slot="action"
                                                slot-scope="row">
                                                    <b-link
                                                    @click="row.toggleDetails"
                                                    class="butMore">
                                                        {{ row.detailsShowing ? '-' : '+'}}
                                                    </b-link>
                                                </template>
                                                <template
                                                slot="row-details"
                                                slot-scope="row">
                                                    <b-row>
                                                        <b-col>
                                                            {{row.item.description_work}}
                                                        </b-col>
                                                    </b-row>
                                                </template>
                                                <template
                                                slot="checkbox"
                                                slot-scope="row">
                                                    <b-form-checkbox />
                                                </template>
                                            </b-table>
                                        </div>
                                    </b-col>
                                </b-row>
                            </b-container>
                        </b-tab>
                    </b-tabs>
                </b-card>
                <b-card
                no-body
                class="gs-container">
                    <b-tabs
                    card >
                        <b-tab
                        title="Tab 3">
                            <container>
                                <container-header>
                                    1
                                </container-header>
                                <container-body>
                                    <b-table
                                    striped
                                    hover
                                    :items="items" />
                                </container-body>
                                <container-footer>
                                    3
                                </container-footer>
                            </container>
                        </b-tab>
                        <b-tab
                        title="Tab 4">
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                            Tab Contents 2<br/>
                        </b-tab>
                        <b-tab
                        :title="`Offer ${i}`"
                        v-for="i in tabs">
                            Offer {{i}}
                        </b-tab>
                    </b-tabs>
                </b-card>
            </b-card-group>
        </container-body>
    </container>
</template>

<script type="text/javascript">
import axios from 'axios';
const items = [
    { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
];
const treeData = [
{
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting"
}, {
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.020', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting 1"
}, {
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.030','description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting 2"
}, {
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.030', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting 3"
},
////////////////////
 {"name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description Head Description Head' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }],
  "subMenu": "tiling 1"
}, {
  "name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
 { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }],
  "subMenu": "tiling 2"
}, {
  "name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }],
  "subMenu": "tiling 3"
}, {
  "name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' },
{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.",
  count:'2', unit: 'Psch.', price: '120', summa:'240', without:'120*', discount:' 20%', status: 'Yes', 'checkbox':'true' }],
  "subMenu": "tiling 4"
}
];
export default {
  props: {
    id: String
  },
  data() {
    return {
      items: items,
      project: {number: null, editor: null, date: null,
      street: null, city: null, zip: null},
      customer: null,
      person: null,
      selectedNode: null,
      treeFilter: '',
      treeOptions: {
        multiple: false,
        filter: {
          plainList: true
        }
      },
      show:false,
      tabs: [],
      tabCounter: 0,
      fieldsPrice: {
        position_number: {
          label: '#',
          sortable: true,
        },
        description_head: {
          label: 'Description Head',
          sortable: true
        },
        action: {
          label: '<i class="fas fa-info" style="font-size:10px"></i>',
          class:'text-center'
        },
        count: {
          label: '=',
          sortable: true
        },
        unit: {
          label: 'Unit',
          sortable: true,
        },
        other: {
          label: '&euro;',
          sortable: true,
          class:'text-center'
        },
        summa:{
          label: '&sum;',
          sortable: true,
        },
        without: {
          label: 'Without',
          sortable: true,
        },
               // discount: {
               // label: 'Discount',
               // sortable: true,
               // },
        status: {
          label: 'Status',
          sortable: true,
        },
        checkbox: {
          label: '%',
          sortable: true,
          class:'text-center'
        }
      },
      add_offer: {
        work:null,
        insurance_number:null,
        place:null,
        comment:null
      },
      works: [
        { value: 'painting', text: 'Painting Works' },
        { value: 'tiling', text: 'Tiling Work'}           
      ],
      // do not judge me :)
      treeData: new Promise(resolve => {
        const items = {}
        treeData.forEach(item => {
          const { name } = item;
          if (false === (name in items)) {
            items[name] = []
          }
          let treeItem = {
            text: item.subMenu ? `${item.subMenu}` : item.name,
            data: item
          }
          items[name].push(treeItem)
        })
        let o = Object.keys(items).reduce((a, b) => {
          let children = items[b]
          let item
          if (children.length > 1) {
            item = {
              text: children[0].data.name,
              data: Object.assign({}, children[0].data),
              children
            }
          }
          else {
            item = children[0]
            item.data
          }
          if (!item.data) {
         //           item.data = {
         //             content: children[0].data.content,
         //             isRoot: true
          //          }
          }
          else {
            item.data.isRoot = true
          }
          a.push(item)
          return a
        }, [])
        resolve(o)
      }),
      area: [
        {
          name: 'Bauverein',
          persons: [{ label:'Sven Wolthoff', mail:'Sven@Wolth-off', tel:'+49 (999) 99-99-99', fax:'+49 (999) 99-99-99'},
          {label:'Michael Wernity', mail:'Michael@Wernity', tel:'+49 (888) 88-88-88'},
          {label:'Sven Schulmeier', mail:'Sven@Schulmeier', tel:'+49 (777) 77-77-77'}]
        },
        {
          name: 'ABG',
          persons: ['Sommer', 'Herbst', 'Winter']
        },
        {
          name: 'Entega',
          persons: ['Alexander Ploety', 'Norbert Staedter', 'Johen Bendt']
        },
      ]
    } //return
  }, //data
  computed: {
    availablePersons() {
      return this.customer ? this.customer.persons : false
    }
  },
  methods: {
    tmouseOver: function(){
      this.show = true;   
    },
    mouseOut:function(){
      this.show=false;
    },
    newTab () {
      this.tabs.push(this.tabCounter++)
    },
    offerOk (){
      axios.get('/add_offer', {params: {
        add_work: this.add_offer.work,
        add_insurance_number: this.add_offer.insurance_number,
        add_place: this.add_offer.place,
        add_comment: this.add_offer.comment
      }}).then(response => {
     console.log(response)
    })
    }
  },
  mounted(){
    axios.get('/project_detail', {params: {id: this.id}}).then(response => {
      this.project.number = response.data.project_number,
      this.project.date = response.data.date,
      this.project.street = response.data.street,
      this.project.city = response.data.city,
      this.project.zip = response.data.zip,
      this.project.editor = response.data.first_name+' '+response.data.second_name
    })
  }
}
</script>
<style>
.warpTree {
  position: relative;
  height: 100%;
}
.navTree {
  position: absolute; 
  left:0;
  right:0;
  top:0;
  bottom:0;
  overflow: auto;
  overflow-x: hidden;
  background-color: #f7f7f7;
  z-index: 9999;
}
.tree-anchor {
  text-decoration: none !important;
  font-size: 12px;
  padding: 0px;
  margin: 0px;
 }
.tree-arrow{
  height: 12px;
}
.tree-arrow.has-child:after{
  height: 7px;
  width: 7px;
  top: 40%;
}
.filter-input{
  padding: 2px;
  margin: 0px;
  width: 70%;
  min-width:125px;
  height: 20px;
  font-size:12px;
}
.slide-leave-active, .slide-enter-active {
  transition: 1s;
}
.slide-enter {
  transform: translate(-100%, 0);
}
.slide-leave-to {
  transform: translate(-100%, 0);
}
.butMore{
  text-decoration: none !important;
  font-size: 15px;
  padding-left: 10px;
  padding-top: 0px;
}
.cForm{
  font-size: 12px;
  height: 20px;
}
.cForm-input{
  font-size: 12px;
  height: 19px;
}
.cForm-inputG{
  height: 19px;
  width: 20px;
  font-size: 10px;
  padding: 0px;
  margin-left: 2px;
}
.cForm-text{
  font-size: 12px;
  margin-top:20px;
}
.cForm-inputBeforG{
  font-size: 12px;
  height: 19px;
}
.v-select {
  height: 12px;
}
.v-select.open .dropdown-toggle {
  height: 12px;
}
.dropdown-toggle .clearfix{
  height: 12px;
}
.v-select .dropdown-toggle .clear{
  bottom: -7px;
  font-size: 18px;
}
.v-select .open-indicator {
  bottom: 4px;
  height: 8px;
  width:  8px;
}
.v-select.searchable .dropdown-toggle {
  height: 15px;
}
.v-select .selected-tag {
  line-height: 4px;
}
.v-select .dropdown-menu {
  font-size: 10px !important; /*or some other pixel value < 160*/
} 
.col-form-label {
  padding: 0px;
}
.b-form-group{
  padding: 0px;
  height: 4px;
}
.customButton{
  padding: 1px;
  font-size: 10px;
  height: 16px;
}
.select{
  font-size: 12px;
  height: 20px !important;
  padding: 0px;
  padding-left: 12px;
  margin: 0px;
}
input[type='number'] {
  -moz-appearance:textfield;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}
</style>