<template>
    <container>
        <b-modal size="lg" centered ok-only id="map" title="Track">
            <b-embed type="iframe" aspect="16by9"
            :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+project.street">
            </b-embed>
        </b-modal>
        <b-form @submit="offerOk"> 
            <b-modal size="md" centered id="addOffer" ref="addOffer" title="Add Offer">
                <b-form-group horizontal :label-cols="4" label="Order Number:" label-for="OrderNumber" style="padding: 5px;">
                    <b-form-input v-model="project.number" class="cForm-input" id="OrderNumber"
                    disabled :state="null" type="text" placeholder="Enter number" />  
                </b-form-group>
                <b-form-group horizontal :label-cols="4" label="Type Of Work:" label-for="work" style="padding: 5px;">
                    <b-form-select class="select" id="work" :options="works" v-model="add_offer.work" required />
                </b-form-group>
                <b-form-group horizontal :label-cols="4" label="Insurance Number:"
                label-for="InsuranceNumber" style="padding: 5px;padding-top: 8px;">
                    <b-form-input class="cForm-input" id="InsuranceNumber" :state="null" type="number"
                    v-model="add_offer.insurance_number" placeholder="Enter number" required />
                </b-form-group>                         
                <b-form-group horizontal :label-cols="4" label="Place:" label-for="place" style="padding: 5px;">
                    <b-form-input class="cForm-input" id="place" placeholder="Enter place"
                    :rows="2" :max-rows="4" required v-model="add_offer.place" />
                </b-form-group>               
                <b-form-textarea class="cForm-text" id="textarea1" placeholder="Enter something"
                :rows="2" :max-rows="6" required v-model="add_offer.comment" />
                <template slot="modal-footer">
                    <b-button type="submit" variant="primary" data-toggle="addOffer" >
                        OK
                    </b-button>
                </template>
            </b-modal>
        </b-form>
        <b-form @submit="nameOfPart"> 
            <b-modal size="md" centered id="addPart" ref="shpart" title="Add Part">
                <b-form-group horizontal :label-cols="4" label="Name of part:"
                label-for="nameofpart" style="padding: 5px;">
                    <b-form-input v-model="nameofpart" required class="cForm-input" id="nameofpart"
                    :state="null" type="text" placeholder="Enter name of part" />  
                </b-form-group>
                <template slot="modal-footer">
                    <b-button type="submit" variant="primary" data-toggle="addPart">
                        OK
                    </b-button>
                </template>
            </b-modal>
        </b-form>

        <container-header class="container-fluid">
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
                                    <b-container>
                                        <b-row>
                                            <b-col sm="6" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm"
                                                label="Project Number:" label-for="project-number">
                                                    <b-form-input id="project-number" :state="null" disabled type="text"
                                                    v-model="project.number" placeholder="Enter project number" class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Date:" label-for="date">
                                                    <b-form-input id="date" :state="null" type="date" v-model="project.date"
                                                    placeholder="Enter date" class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Editor:" label-for="editor">
                                                    <b-form-input id="editor" :state="null" type="text" v-model="project.editor"
                                                    placeholder="Enter editor name" class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
                                            <b-col sm="6" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4"
                                                class="cForm" label="Street:" label-for="street">
                                                    <b-input-group>
                                                        <b-form-input id="street" :state="null" type="text" v-model="project.street"
                                                        placeholder="Enter street" class="cForm-inputBeforG" />
                                                        <b-button v-b-modal.map class="cForm-inputG">
                                                          G
                                                        </b-button>
                                                    </b-input-group>
                                                </b-form-group>   
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="City:" label-for="city">
                                                    <b-form-input id="city" :state="null" type="text" v-model="project.city"
                                                    placeholder="Enter city" class="cForm-input" />
                                                </b-form-group>   
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Zip code:" label-for="zip-code">
                                                    <b-form-input id="zip-code" :state="null" type="text" v-model="project.zip"
                                                    placeholder="Enter zip code" class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
                                        </b-row>
                                        <hr />
                                        <b-row> 
                                            <b-col sm="6" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Customer:" label-for="customer">
                                                    <v-select taggable label="name" v-model="customer" :options="area" />
                                                </b-form-group> 
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Contact person:"
                                                label-for="contact-person" v-if="availablePersons">
                                                    <v-select taggable v-model="person" :options="availablePersons" />
                                                </b-form-group> 
                                            </b-col>
                                            <b-col sm="6" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="E-mail:" v-if="person" >
                                                    <b-button class="customButton" :href="'mailto:'+person.mail">
                                                        {{person.mail}}
                                                    </b-button>
                                                </b-form-group> 
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Phone:" v-if="person">
                                                    <b-button class="customButton" :href="'cal:'+person.tel">
                                                        {{person.tel}}
                                                    </b-button>
                                                </b-form-group> 
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Fax:" v-if="person">
                                                    <b-button class="customButton" :href="'cal:'+person.fax">
                                                        {{person.fax}}
                                                    </b-button>
                                                </b-form-group>
                                            </b-col>
                                        </b-row>
                                        <hr />
                                        <b-row>
                                            <b-col>
                                                <b-button class="customButton" v-b-modal.addOffer @click="
                                                                                                        add_offer.comment=null,
                                                                                                        add_offer.place=null,
                                                                                                        add_offer.insurance_number=null,
                                                                                                        add_offer.work=null"> <!--@click.prevent="newTab"-->
                                                    Add Offer
                                                </b-button>   
                                                <b-button class="customButton">
                                                    Add Assignment
                                                </b-button> 
                                                <b-button class="customButton">
                                                    Add Invoice
                                                </b-button>
                                            </b-col>   
                                        </b-row>
                                    </b-container>   
                                    <!-------------------------------------------------------------->
                                    <b-table class="tableProject" striped hover :items="offers" :fields="fieldsOffer" @row-clicked="inItemClick" >
                                        <template slot="offer_number" slot-scope="offer" >
                                                {{  offer.item.offer_number }}
                                        </template>
                                        <template slot="status_set" slot-scope="offer">
                                            <b-form inline>
                                                <b-form-select v-model="offer.item.status_set" :options="options"/>
                                                <i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyleOffer(offer.item.status_set)"></i>
                                            </b-form>
                                        </template>
                                        <template slot="delete" slot-scope="offer">
                                                <b-col align-self="center"><b-link @click="offerDel(offer.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" /></b-col>
                                        </template>
                                    </b-table>
                                </container-body>
                            </container>
                        </b-tab>
                        <b-tab title="Price List" style="padding:0px;">
                            <b-container class="warpTree">
                                <transition name="slide">
                                    <b-col cols="2" class="navigation navTree" style="padding:0px;border-right: 1px solid #dee2e6;" 
                                    id="mySidenav" v-show="show" @mouseleave="mouseOut">
                                        <div class="navigation navTree" >
                                            <div class="navigation-filter" align="center" style=" padding-top: 10px;">
                                                <input type="text" class="filter-input" v-model="treeFilter" placeholder="Type to filter...">
                                            </div>
                                            <div class="navigation-tree">
                                                <tree :data="treeData" :options="treeOptions" :filter="treeFilter" v-model="selectedNode">
                                                    <div class="tree-scope" slot-scope="{ node }">
                                                        <template v-if="node.data.isRoot">
                                                            <span class="text" style="font-size:14px">
                                                                {{ node.text }}
                                                            </span>
                                                        </template>
                                                        <template v-else>
                                                            <span class="text">
                                                                {{ node.text }}
                                                            </span>
                                                        </template>
                                                    </div>
                                                </tree>
                                            </div>
                                        </div>
                                    </b-col>
                                </transition>
                                <b-row style="height:100%;">
                                    <div @click="tmouseOver"
                                    style="height:100%;cursor:pointer;background-color:#f7f7f7;
                                    padding:5px;display:flex;align-items:center;border-right:1px solid #dee2e6;">
                                        <i class="fas fa-angle-right" />
                                    </div>
                                    <b-col class="contentTree" style="padding-top:8px;">
                                        <div>
                                            <div v-if="!selectedNode || selectedNode.hasChildren()">
                                                Select the menu item
                                            </div>
                                            <!-- ------------------------------------------------- -->
                                            <b-table v-else :items="selectedNode.data.content" :fields="fieldsPrice" 
                                            class="tableProject" hover @row-dblclicked="inItemClickPrice" small>
                                                <template slot="action" slot-scope="row">
                                                    <b-link @click="row.toggleDetails" class="butMore">
                                                        {{ row.detailsShowing ? '-' : '+'}}
                                                    </b-link>
                                                </template>
                                                <template slot="row-details" slot-scope="row">
                                                    <b-row>
                                                        <b-col>
                                                            {{row.item.description_work}}
                                                        </b-col>
                                                    </b-row>
                                                </template>
                                                <template slot="checkbox" slot-scope="row">
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
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Edit Offer">
                            <container>
                                <container-header>
                                </container-header>
                                <container-body><!-- <b-container v-show="tmp.number != null">  <b-container> -->
                                    <b-container v-show="tmp.number != null">
                                        <b-row>
                                            <b-col sm="6" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm"
                                                label="Offer Number:" label-for="offer-number">
                                                    <b-form-input id="offer-number" :state="null" disabled type="text" v-model="tmp.number"
                                                    placeholder="Enter offer number" class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Date:" label-for="date">
                                                    <b-form-input id="date" :state="null" type="date" v-model="tmp.date"
                                                    placeholder="Enter date" class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Place:" label-for="place">
                                                    <b-form-input id="place" :state="null" type="text" v-model="tmp.place"
                                                    placeholder="Enter place" class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
                                            <b-col sm="6" class="cuestomRow">
                                             <b-form-group horizontal :label-cols="4" class="cForm" label="Insurance Number:" label-for="insurance">
                                                    <b-form-input id="insurance" :state="null" type="text" v-model="tmp.insurance"
                                                    placeholder="Enter insurance namber" class="cForm-input" />
                                                </b-form-group>  
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Other:" label-for="other">
                                                    <b-form-input id="other" :state="null" type="text" v-model="tmp.other"
                                                    placeholder="Enter other" class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
                                        </b-row>
                                        <b-row>
                                            <b-col>
                                                <b-button class="customButton" v-b-modal.addPart>
                                                     Add Part
                                                </b-button>   
                                            </b-col>   
                                        </b-row>                                       
<!-- ----------------------------------------------------------------------- -->
                                       <label style="width:100%" v-for="(part, index) in partx" >
                                           <b-form-checkbox  plain name="partx" class="withoutbox" :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }"
                                            :value="part.parts.part_name+index"  @change="toggleItem(part.parts.part_name+index)">
                                        {{part.parts.part_name}}
                                        <b-link @click="partDel(part.parts.part_name +index)" class="fas fa-trash fa-w-16" />
                                    </b-form-checkbox>
                                            <table  class="tableProject table b-table table-striped withoutmargin table-hover"
                                            :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }">

<tr>
    <th class="sorting" style="width:10%">#</th>
    <th class="sorting text-center" style="width:20%">Description Head</th>
    <th class="text-center" style="width:5%"><i class="fas fa-info" style="font-size:10px"></i></th>
    <th class="sorting text-center" style="width:5%">=</th>
    <th class="sorting text-center" style="width:10%">Unit</th>
    <th class="sorting text-center" style="width:10%">€</th>
    <th class="sorting text-center" style="width:10%">∑</th>
    <th class="sorting text-center" style="width:10%">Without</th>
    <th class="sorting text-center" style="width:10%">Status</th>
   <!-- <th class="sorting text-center">%</th>-->
    <th class="sorting text-center" style="width:10%">Delete</th>
</tr>

                                                <tbody v-for="(content, subIndex) in part.parts.part_content">
                                                    <tr>
                                                    <td class="text-center">
                                                    {{content.position_number}}</td>
                                           <!--    <td>{{content.сheckbox}}</td> -->
                                               
                                                <td class="text-center">
                                                    <b-input type="text" placeholder="Description Head" class="cForm-input"
                                                    :value="content.description_head" />

                                                </td>
                                             <!--    <td>{{content.description_work}}</td>-->
                                             <td class="text-center">   <b-link v-b-toggle="'desk_worck'+index+subIndex" class="butMore">
                                                    <span class="when-opened">-</span>
                                                    <span class="when-closed">+</span>
                                             </b-link>
                                                  
                                             </td>


                                                 <td class="text-center">
                                                    <b-input type="number" placeholder="Count" class="cForm-input"
                                                                                                        :value="content.count" />
                                                 </td>
                                                 <td class="text-center" @click.prevent.self>

                                                   <b-input type="text" placeholder="Count" class="cForm-input"
                                                                                                        :value="content.unit" />
                                                     <!--   <v-select taggable :options="['foo','bar','baz']"></v-select>-->

                                              <!--  <td>{{content.discount}}</td>-->
                                                
                                                <td class="text-center">
                                                    <b-input type="number" placeholder="Price" class="cForm-input"
                                                    :value="content.price" />
                                            </td>
                                              <!--      <td class="text-center">{{content.summa}}</td> -->
                                                   <td class="text-center">{{content.count * content.price}}</td> 
                                                <td class="text-center">{{content.without}}</td>
                                                <td class="text-center">{{content.status}}</td>
                                               <!-- <td>{{content.summa}}</td> -->
                                                                                                
                                                <td class="text-center"> <b-link @click="subPartDel(part.parts.part_name+index, subIndex)" class="fas fa-trash fa-w-16" /></td>
                                                </tr> 
                                             <tr>
                                                    <td colspan="10" @click.prevent.self >  
                                                       <b-collapse style="width:100%" :id="'desk_worck'+index+subIndex"  contenteditable ="true">
                                                            {{content.description_work}}  
                                                        </b-collapse>
                                                    </td> 
                                                </tr>
                                         
                                            </tbody>   
                                            </table>
                                        </label>
<!-- ----------------------------------------------------------------------- -->
                                    </b-container>
                                </container-body>
                                <container-footer>
                                    3
                                </container-footer>
                            </container>
                        </b-tab>
                        <b-tab title="Tab 4">
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
                        <b-tab :title="`Offer ${i}`" v-for="i in tabs">
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
const partx = [
{parts:{part_name:'part1', part_content:[{
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Psch.',
without:'120*'
},
{
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Psch.',
without:'120*'
},

]}},
{parts:{part_name:'part2', part_content:[{
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Psch.',
without:'120*'
}]}},
{parts:{part_name:'part3', part_content:[{
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Psch.',
without:'120*'
}]}}
]
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
const worksinside = [
    { checkbox: null, count: null, description_head: null,
    description_work: null,  discount: null, position_number: null, price: null, status: null, summa: null, unit: null, without: null}
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
      toggle: [],
      partx: partx,
      items: items,
      worksinside: worksinside,
      nameofpart: null,
      shpart: null,
      fieldsOffer: {
                offer_number: {
                label: 'Offer No.',
                sortable: true
                },
                date: {
                label: 'Date',
                sortable: true
                },
                place: {
                label: 'Place',
                sortable: true
                },
                insurance_number: {
                label: 'Insurance Number',
                sortable: true
                },
 
                other: {
                label: 'Other',
                sortable: true
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'status'
                },
                delete: {
                label: 'Delete',
                }
                },
               options: [
                         { value: 'Open', text: 'Open' },
                         { value: 'Done', text: 'Done'},
                         { value: 'Invoice', text:'Invoice' },
                         { value: 'Desiccation', text:'Desiccation' },
                         { value: 'Leakage_Detection', text:'Leakage Detection' },
                         { value: 'Restoration', text:'Restoration'}
               ],     
      offers: [],

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
      count_offer_number: 0,
      works: [
        { value: 'painting', text: 'Painting Works' },
        { value: 'tiling', text: 'Tiling Work'}           
      ],
     

tmp:{
    number:null,
    date:null,
    place:null,
    insurance:null,
    work:null,
    other:null,
    parts:null
},


//tmp:{
// parts:null
//},

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
  inItemClick(item, index, event) {
       // console.log(item),
        //this.tmp = item.parts,
        this.tmp.number = item.offer_number,
        this.tmp.date = item.date,
        this.tmp.place = item.place,
        this.tmp.insurance = item.insurance_number,
        this.tmp.work = item.work,
        this.tmp.other = item.other
        },
        inItemClickPrice(item, index, event) {
        this.toggle.filter(function (valueToggle) {
            partx.filter(function (valuePart, index) {
                if(valuePart.parts.part_name+index == valueToggle){
                valuePart.parts.part_content.unshift(
                   { //сheckbox:item.checkbox,
                    position_number:item.position_number,
                   
                    description_head:item.description_head,
                    description_work:item.description_work,
                    count:item.count,
                    discount:item.discount,
                    
                    price:item.price,
                    status:item.status,
                    summa:item.summa,
                    unit:item.unit,
                    without:item.without,
                    }); 
                } 
            });
        });

    



        },
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
        add_number: this.project.number,
        add_insurance_number: this.add_offer.insurance_number,
        add_place: this.add_offer.place,
        add_work: this.add_offer.work,
        add_comment: this.add_offer.comment,
        add_project_id: this.id
      }}).then(response => {
   //  console.log(response)
    }),
      this.$refs.addOffer.hide(),
       axios.get('/offers', {params: {id: this.id}}).then(response => {
      this.offers = response.data
   })
    },
    offerDel(del_id){
        if(confirm("Are you sure?")){axios.get('/del_offer', {params: {id: this.id, del_id: del_id}}).then(response => {
        this.offers = response.data
       })};
 
    },
    computeStyleOffer(value) {
        switch (value) {
                case 'Open': return {'color': '#F5DEB3'};
                case 'Done': return {'color': 'green'};
                case 'Invoice': return {'color':'orange'};
                case 'Desiccation': return {'color':'grey'};
                case 'Leakage_Detection': return {'color':'red'};
                case 'Restoration': return {'color':'blue'};
            }
        },
        nameOfPart(){
            this.shpart = true;
            this.$refs.shpart.hide(),
            this.partx.unshift(
               {parts:{part_name: nameofpart.value, part_content:[]}}
               )},

         toggleItem: function (key) {
        var i = this.toggle.indexOf(key)
        if (i < 0) {
        this.toggle.push(key)
      } else {
        this.toggle.splice(i, 1)
      }
    },
    partDel(del_id){
       // console.log(del_id);
              if(confirm("Are you sure?"))partx.filter(function (valuePart, index) {
                if(valuePart.parts.part_name+index == del_id){
                       partx.splice(index, 1);
                } 
        });
    },
    subPartDel(del_id, subDel_id){
       // console.log(del_id);
              if(confirm("Are you sure?"))partx.filter(function (valuePart, index) {
                if(valuePart.parts.part_name+index == del_id){
                   valuePart.parts.part_content.splice(subDel_id, 1);
                      
                } 
        });
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
    }),
    axios.get('/offers', {params: {id: this.id}}).then(response => {
      this.offers = response.data
    //  this.offers.date = response.data[0].date,
    //  this.offers.id = response.data.id,
    //  this.offers.insurance_number = response.data.insurance_number,
    //  this.offers.status_set = response.data.status_set,
    //  this.offers.offer_number = response.data.offer_number,
    //  this.offers.other = response.data.other,
    //  this.offers.place = response.data.place,
    //  this.offers.work = response.data.work,
  //    console.log(response.data),
   //   console.log(this.offers)
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
.withoutbox input[type=checkbox]{
display:none;
}
.withoutmargin{
    margin-bottom: 0px !important;
}

.collapsed > .when-opened,
:not(.collapsed) > .when-closed {
  display: none;
}
</style>