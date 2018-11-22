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
         <b-modal size="sm" centered id="move" ref="move" title="Move">
                <b-form-select multiple class="" id="move" @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" :select-size="4">
                    <option v-for="part in partx">{{part.parts.part_name}}</option>
                </b-form-select>
                <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="['Move', 'Copy']" />
          <template slot="modal-footer">
                    <button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>
                    <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button>
                </template>
            </b-modal>
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
                        <b-tab title="Price List" style="padding:0px;" @keyup.enter="keyupMethod">
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
                                          
                                             <b-form-group horizontal :label-cols="4" class="cForm" label="Insurance Number:" label-for="insurance">
                                                    <b-form-input id="insurance" :state="null" type="text" v-model="tmp.insurance"
                                                    placeholder="Enter insurance namber" class="cForm-input" />
                                                </b-form-group>  
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Other:" label-for="other">
                                                    <b-form-input id="other" :state="null" type="text" v-model="tmp.other"
                                                    placeholder="Enter other" class="cForm-input" />
                                                </b-form-group>
                                            </b-col>
<b-col sm="6" class="cuestomRow">
    <b-form-row>
        <b-col cols="4"  class="cForm-input">
            Discont:
        </b-col>
          <b-col cols="3">                   <b-input-group class="cForm-input"> 
                                                    <b-input id="disc" type="number" v-model="discP" @input="discOfPercent" :state="null" 
                                                    placeholder="Summa of Percent" class="cForm-input"/>
                                                     <b-input-group-append >
       
      <div class="input-group-text" @click="butDiscPerc = (butDiscPerc == '%' ? 'P' : '%');discOfPercent()">{{butDiscPerc}}</div>
     

    </b-input-group-append>
                                        </b-input-group>
                                            
                                         </b-col>

            <b-col cols="5">                                 <b-input-group append="€"   class="cForm-input">                     
                                                        <b-input disabled id="sop" v-model="disc"  :state="null"  type="text"
                                                        placeholder="Summa of Percent" class="cForm-input text-right" />
                                                    </b-input-group>
    </b-col>
    </b-form-row>
    <b-form-group horizontal :label-cols="7" class="cForm" label="Netto:" label-for="netto">
        <b-input-group append="€"  class="cForm-input">  
                                                    <b-form-input id="netto" v-model="netto" :state="null"  type="text" 
                                                    placeholder="Enter netto" disabled class="cForm-input text-right" />
                                                </b-input-group>
                                                </b-form-group>
    <b-form-row>

        <b-col cols="3"  class="cForm-input">
            Added tax:
        </b-col>
                  <b-col cols="1"  class="cForm-input">
            <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'addtax'">
                                                    <span class="when-closed">+</span>
                                                   
                                                    
            </b-link>
        </b-col>
          <b-col cols="3">                               <b-input-group append="%"  class="cForm-input">  
                                                    <b-input id="taxP" @input="discOfPercent" v-model="taxP" :state="null"  type="number"
                                                    placeholder="Summa of Percent" class="cForm-input " />
                                                </b-input-group>
                                            
                                         </b-col>

            <b-col cols="5">                                 <b-input-group append="€"  class="cForm-input">                     
                                                        <b-input disabled id="tax" v-model="tax" :state="null"  type="text"
                                                        placeholder="Summa of Percent" class="cForm-input text-right" />
                                                    </b-input-group>
    </b-col>
    </b-form-row>
    <b-collapse style="width:100%" id="addtax" v-model="addtaxColapse">
       
    <b-form-row>

        <b-col cols="3"  class="cForm-input calttax">
            Added tax:
        </b-col>
                    <b-col cols="1"  class="cForm-input">
            <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'addtax'">
                                                 
                                                    <span class="when-opened">-</span>
                                                    
            </b-link>
        </b-col>
          <b-col cols="3">                               <b-input-group append="%"  class="cForm-input">  
                                                    <b-input id="taxP" @input="discOfPercent" v-model="taxP2" :state="null"  type="number"
                                                    placeholder="Summa of Percent" class="cForm-input " />
                                                </b-input-group>
                                            
                                         </b-col>

            <b-col cols="5">                                 <b-input-group append="€"  class="cForm-input">                     
                                                        <b-input disabled id="tax" v-model="tax2" :state="null"  type="text"
                                                        placeholder="Summa of Percent" class="cForm-input text-right" />
                                                    </b-input-group>
    </b-col>
    </b-form-row>
</b-collapse>
        <b-form-group horizontal :label-cols="7" class="cForm" label="Brutto:" label-for="brutto">
        <b-input-group append="€"  class="cForm-input">  
                                                    <b-form-input id="brutto" v-model="brutto" :state="null"  type="text"
                                                    placeholder="Enter brutto" disabled class="cForm-input text-right" />
                                                </b-input-group>
                                                </b-form-group>
</b-col>
</b-row> 
                                            </b-col>
                                        </b-row>
                                        <b-row>
                                            <b-col>
                                                <b-button class="customButton" v-b-modal.addPart>
                                                     Add Part
                                                </b-button>   
                                                <b-button class="customButton" @click="move">
                                                     Move
                                                </b-button>   
                                            </b-col>   

                                        </b-row>                                       
<!-- ----------------------------------------------------------------------- -->
<draggable v-model="partx" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}" :no-transition-on-drag="true" @start="drag=true" @end="drag=false">
                                       <div style="width:100%" v-for="(part, index) in partx" :key="part.id">
                                        
                                            

   <b-form-checkbox  style="width:100%" plain name="partx" class="withoutbox handleTitle" :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }"
                                            :value="part.parts.part_name+index"  @change="toggleItem(part.parts.part_name+index)">



            <b-link v-b-toggle="'partx' + index" class="butMore" style="width:100%">
               <span class="when-opened">-</span>
               <span class="when-closed">+ {{ thousandSeparator(total(part.parts.part_content)) }} €</span>
            </b-link>
  <i class="fas fa-dot-circle" style="font-size:12px"></i> 
     <span contenteditable="true" @input="toModel($event, index)" @click.prevent.self>{{part.parts.part_name}}</span>
    <b-link class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="partDel(part.parts.part_name+index);discOfPercent()"/>
    

   </b-form-checkbox>
          
<b-collapse :id="'partx'+index">
    <div  :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }">
<div>
    
                                            <b-form-row>
                                                <div class="tnumber text-center">#</div>
                                                <div class="tposition text-center">Position</div>
                                                <div class="tdeschead text-center" :style="'width:'+computedWithDesc(part.parts.checkbox_list.flavours)+'%'">Description Head</div>
                                                <div class="tinfo text-center"><i class="fas fa-info" style="font-size:10px;width:10px;padding:0px;"></i></div>
                                                <div class="tcount text-center">=</div>
                                                <div class="tunit text-center">Unit</div>
                                                <div class="tprice text-center">€</div>
                                                <div class="tsumm text-center">∑</div>
                                              
                                                <div class="custom-control-inline tpercent">
                                                    <div  v-for="(select_from_allSelected, key) in part.parts.checkbox_list.allSelected" class="ccbox" :class="classRow(part.parts, key)">                                                    
                                                        <b-form-checkbox plain v-model="part.parts.checkbox_list.allSelected[key]"
                                                   
                                                        @change="toggleAll($event, key, part.parts.checkbox_list, part.parts.part_content)"
                                                        class="withoutPad"
                                                         />
                                                     </div>

                                                </div>
                                                  <div class="twithout text-center"  v-if="butDiscPerc=='%'">-%</div>
                                                <div class="tcalc text-center">Calculation</div>
                                                <div class="tdelete text-center">X</div>

                                           </b-form-row>

</div>

<draggable v-model="part.parts.part_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}" :no-transition-on-drag="true" @start="drag=true" @end="drag=false">


     <div v-for="(content, subIndex) in part.parts.part_content" :class="colorIdent(part.parts.part_name, subIndex)">
                                <b-form-row style="height:20px;" @mouseover="content.upHere = true" @mouseleave="content.upHere = false" 
                                            :class="{howerRow: content.upHere, '': !content.upHere}" 
                                            :key="content.id" >

                                                    <div  class="tnumber text-center" :class="(content.unit=='%') ? '' : 'handle'" style="font-weight: normal;" 
    @click="content.upHere = false; selectRow(part.parts.part_name, subIndex)">
    {{(subIndex+1)}}
    </div>
<div  class="tposition text-center">
                                                   <b-input @click.prevent.self type="text" placeholder="Unit" class="cForm-input cinput" v-model="content.position_number" />
                                               </div>
                                           <!--    <td>{{content.сheckbox}}</td> -->
                                               
                                                <div class="tdeschead text-center" :style="'width:'+computedWithDesc(part.parts.checkbox_list.flavours)+'%'">
                                                    <b-input  @click.prevent.self type="text" placeholder="Description Head" class="cForm-input"

                                                    v-model="content.description_head" />

                                              </div>
                                             <!--    <td>{{content.description_work}}</td>-->
                                             <div  class="tinfo text-center">   <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'desk_worck'+index+subIndex">
                                                    <span class="when-opened" :style="'color:'+computedStylePlus(content.description_work)">-</span>
                                                    <span class="when-closed" :style="'color:'+computedStylePlus(content.description_work)">+</span>
                                             </b-link>
                                                  
                                             </div>


                                                 <div  class="tcount text-center">
                                                    <b-input @click.prevent.self @input="discOfPercent" type="number" placeholder="Count" class="cForm-input ainput"
                                                                                                        v-model="content.count" />
                                                 </div>
                                                 <div  class="tunit text-center">
                                                 <!--  <input @click.prevent.self type="text" placeholder="Unit" class="cForm-input ainput form-control"
                                                   v-model="content.unit" @input="persent(content.unit, subIndex, part.parts.checkbox_list, part.parts.part_content.length)" />
                                                -->
                                                <b-select v-model="content.unit" @input="persent(content.unit, subIndex, part.parts.checkbox_list, part.parts.part_content.length)" class="select" style="min-width:45px">
                                                            <option v-for="opt in unit_type" :disabled="disOptPercent(part.parts.part_content, opt)">
                                                                    {{opt}} 
                                                            </option>
                                                </b-select>   
                                                <!-- input вызывает несколько раз   <v-select taggable :options="['foo','bar','baz']"></v-select>-->
                                                    
                                              <!--  <td>{{content.discount}}</td>-->
                                           
                                                </div>
                                                <div class="tprice text-right" style="font-weight: normal;">
                                                    
                                                    <input v-if="content.unit!='%'" @click.prevent.self @input="discOfPercent" type="number" placeholder="Price" class="cForm-input form-control rinput"
                                                    v-model="content.price"/>
                                                 
                                                   <div v-else> {{persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, 'summ')}}</div>
                                            </div>
                                              <!--      <td class="text-center">{{content.summa}}</td> -->
                                                   <div  class="tsumm text-right " style="font-weight: normal;" v-if="addtaxColapse==true">
<div :style="content.status=='yes' ? '' : 'color:grey'"
:class="{ 'calttax': alttax[subIndex] }"
@click="alttax[subIndex] = alttax[subIndex] ? false : true; discOfPercent()">


<div v-if="content.unit!='%'" :title="thousandSeparator(content.count * content.price)"> {{thousandSeparator(content.count * content.price)}}</div>
<div v-else class="text-right" :title="thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))"> {{thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))}} </div>
</div>

</div>
<div v-else  class="tsumm text-right" style="font-weight: normal;" >
    <div :style="content.status=='yes' ? '' : 'color:grey'">

<div v-if="content.unit!='%'" :title="thousandSeparator(content.count * content.price)"> {{thousandSeparator(content.count * content.price)}} </div>
<div v-else :title="thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))"> {{thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))}}</div>
</div>
</div>
                                                  
                                           
                                          
                                                 <div class="custom-control-inline tpercent">
                                             
<div  v-for="(select_from_allSelected, key) in part.parts.checkbox_list.allSelected" >
<div v-for="(opt, indexSelect) in part.parts.checkbox_list.flavours[key]" v-if="indexSelect==subIndex" class="ccbox" :class="classRow(part.parts, key)">

 <b-form-checkbox type="checkbox" plain
:disabled="boxDisable(content.unit, key, indexSelect)"
v-model="part.parts.checkbox_list.selected[key]"
:value="opt" 
class="withoutPad"
@change="box($event, key, indexSelect)"
/>

</div>
</div>
                                              </div>

                                                <div  class="twithout text-center ccbox"  v-if="butDiscPerc=='%'">
                                                    <b-form-checkbox class="withoutPad"  @input="discOfPercent" plain style="margin: 0px;" v-model="content.without"/> 
                                                    
                                                   <!-- <div @click="content.without = content.without ? false : true; discOfPercent()">
                                                        <i style="font-size:13.5px;" class="far fa-check-square" v-if="content.without"></i>
                                                        <i  style="font-size:13.5px;" class="far fa-square" v-else></i>
                                                    </div> -->
                                                </div>
                                               <div  class="tcalc text-center">
<b-form-select @input="discOfPercent" class="select" style="min-width:45px" :options="calc" v-model="content.status" />
</div>
                                               <!-- <td>{{content.summa}}</td> -->
                                                                                                
                                                <div class="tdelete text-center">
                                                  <b-link @click="subPartDel(part.parts.part_name+index, subIndex);discOfPercent()" class="fas fa-trash fa-w-16" />
                                              </div>
                                                </b-form-row>
                                             <b-form-row >
                                                    <b-col cols="12" @click.prevent.self style="width:10%">  
                                                       <b-collapse style="width:100%" :id="'desk_worck'+index+subIndex">
                                                                <vue-editor
                                                                :id="('t'+index + 'x' + subIndex)"
                                                                :ref="('t'+index + 'x' + subIndex)"
                                                                 v-model="content.description_work"
                                                                 :value="content.description_work" >
                                                                 </vue-editor>

                                                              <!--  <b-form-textarea
                                                                 :ref="('t'+index + 'x' + subIndex)"
                                                                 v-model="content.description_work"
                                                                 :rows="3"
                                                                 :max-rows="6"
                                                                 class="cForm-input " /> -->
                                                                 <b-link v-b-toggle="'desk_worckI'+index+subIndex" class="butMore"  v-if="content.description_from_price.length>0">
                                                    <span class="when-opened" >-</span>
                                                    <span class="when-closed">+</span>
                                             </b-link>
                                                       <b-collapse style="width:100%;font-size: 12px;" :id="'desk_worckI'+index+subIndex" v-if="content.description_from_price.length>0">
                                                        {{content.description_from_price}}
                                                       </b-collapse>       
                                                        </b-collapse>
                                                    </b-col> 
                                                </b-form-row>
                                               
                         </div>
                       
      </draggable> 
       
   
      
    </div>
 
                                                
                                                   <b-row class="ttotalsumm">
                                                 
<b-col align-self="end" class="text-right" style="margin-right:20.4%">General {{ thousandSeparator(total(part.parts.part_content)) }}</b-col>
                                              
                                                
                                                </b-row>
<span style="color:grey"> <b-row class="ttotalsumm"> <b-col align-self="end" class="text-right" style="margin-right:20.4%">Alternative {{thousandSeparator(alttotal(part.parts.part_content))}}</b-col>
                                                  </b-row></span>
                                               
                                      
                                    
                                         <br>
</b-collapse>                                 </div>
</draggable>


<calc-table-group :partx="partx"></calc-table-group>
<hr />
    <vue-editor
    id="refCommentOfTable1"
    ref="refCommentOfTable1"
    v-model="commentOfTable"
    >
    </vue-editor>

<!-- <b-form-textarea
ref="refCommentOfTable"
placeholder="Enter comments"
v-model="commentOfTable"
:rows="3"
:max-rows="6"
class="cForm-input" />-->
<!-- ----------------------------------------------------------------------- -->









                                    </b-container>
                                </container-body>
                                <container-footer>
<b-container>
                                      <b-input-group append="€"  class="cForm-input">  
                                                    <b-form-input id="netto" :value="'General: '+thousandSeparator(alltotal(partx)) + '; ' + 'Alternative: '+thousandSeparator(altalltotal(partx))+';'" :state="null"  type="text" 
                                                    placeholder="Enter netto" disabled class="cForm-input text-right" />
                                                </b-input-group>
                                                </b-form-group>
                                    </b-container>
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
import draggable from 'vuedraggable';
import axios from 'axios';
import {  VueEditor, Quill  } from 'vue2-editor';

var partx = [
{parts:{part_name:'part1',

checkbox_list: {
   flavours: {},
    selected: {},
    allSelected: {},
    indeterminate: {}
}, 

part_content:[{
upHere : false,
сheckbox:'true',
count:'1',
description_head:'headDesk',
description_work:'',
description_from_price: '',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'3',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'4',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'5',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},

]}},

{parts:{part_name:'part2',

checkbox_list: {
   flavours: {},
    selected: {},
    allSelected: {},
    indeterminate: {}
}, 

part_content:[{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},

]}},

{parts:{part_name:'part3',

checkbox_list: {
   flavours: {},
    selected: {},
    allSelected: {},
    indeterminate: {}
}, 

part_content:[{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},

]}},
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
    { checkbox: null, count: null, description_head: null, description_from_price: null,
    description_work: null,  discount: null, position_number: null, price: null, status: null, summa: null, unit: null, without: null}
];
  
const treeData = [
{
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting"
}, {
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.020', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting 1"
}, {
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.030','description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting 2"
}, {
  "name": "Painting works",
  "content": [{ 'position_number': '01.05.030', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }
  ],
  "subMenu": "Painting 3"
},
////////////////////
 {"name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description Head Description Head' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }],
  "subMenu": "tiling 1"
}, {
  "name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
 { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }],
  "subMenu": "tiling 2"
}, {
  "name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
  { 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }],
  "subMenu": "tiling 3"
}, {
  "name": "tiling work",
  "content": [{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' },
{ 'position_number': '01.05.010', 'description_head':'Head Description' ,'description_work': "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", 'description_from_price' : "123",
  count:'2', unit: 'Ps.', price: '120', summa:'240', without: false, discount:' 20%', status: 'yes', 'checkbox':'true' }],
  "subMenu": "tiling 4"
}
];
export default {
    components: {
        draggable,
        VueEditor
    },
  props: {
    id: String
  },
  data() {
    return {
        addtaxColapse: false,
        alttax:[],
        unit_type:['Psch.', '%', 'Stück.', 'Sack.'],
        calc:['yes', 'no', 'etc', 'alternative'],
        butDiscPerc: '%',
        disc:0,
        discP:10,
        tax:0,
        tax2:0,
        taxP:19,
        taxP2:0,
        netto:0,
        brutto:0,
   persentCounter:0,
        counter: -1,
        moveToCopyRadio: 'Move',
        moveToCopy:[],
        tmpArr:[],
        oldColor:[],
        color:[],
      disable: [],
      toggle: [],
      partx: partx,
      items: items,
      worksinside: worksinside,
      nameofpart: null,
      shpart: null,
      fieldsOffer: {
                offer_number: {
                label: 'Offer Number',
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
          label: 'Position Number',
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
commentOfTable: 'something',


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
      ],
    } //return
  }, //data
  
  computed: {


    computedStylePlus: function () {
      var vm = this;
      return function (val) {
  
        if (val.length>0){
            return 'blue;'
        } else{
            return 'gray;'
        }

      }
    },

    colorIdent: function () {
      var vm = this;
      return function (part, subIndex) {
           if (this.color.indexOf(part+'-'+subIndex) != -1 ){
                return 'greenrow'
           } else{
                return ''
           }
         // return this.color[part+'-'+subIndex] ? 'green' : '';
      }
    },
computedWithDesc: function () {
      var vm = this;
      return function (val) {
        var w = 35;
        var count = 0;
          for (var obj in val) { 
             if(count==0){
                w=w+0.6
             }
             if(count>=2){
                w=w-1.7
             }
                w=w-0.6
                count++
            }
        
        return w;
      }
    },

    availablePersons() {
      return this.customer ? this.customer.persons : false
    },

    alltotal: function () {
      var vm = this;
      return function (value) {

        var summa=0
        value.forEach(function (val) {
            val.parts.part_content.forEach(function (val1) {
            if (val1.status=='yes') {
            summa+=val1.count * val1.price
            }
            })
        })

          return summa;
      };
   },
altalltotal: function () {
      var vm = this;
      return function (value) {

        var summa=0
        value.forEach(function (val) {
            val.parts.part_content.forEach(function (val1) {
            if (val1.status!='yes') {
            summa+=val1.count * val1.price
            }
            })
        })

          return summa;
      };
   },
    total: function () {
      var vm = this;
      return function (value) {
        var summa=0
        value.forEach(function (val) {
             if (val.status=='yes') {
            summa+=val.count * val.price
        }
        })
          return summa;  //количество разрядов
      };
   },
    alttotal: function () {
      var vm = this;
      return function (value) {
        var summa=0
        value.forEach(function (val) {
             if (val.status!='yes') {
            summa+=val.count * val.price
        }
        })
          return summa;  //количество разрядов
      };
   },
    persent_to_str: function(){
        var vm = this;
        return function (subIndex, all_obj, selected, content, summOrPercent){
            var summa=0
            for (var obj in all_obj) {

                if(selected[obj].indexOf('temp'+(subIndex+1))!=-1){
                    selected[obj].forEach(function(val, index){
                        if (val!='temp'+(subIndex+1)){
                            val=val.split('temp')
                            val[1]--

                                summa += content[val[1]].count*content[val[1]].price
                            
                        }
                    })
                }

            }

        var persent_from_summa = ((summa/100)*content[(subIndex)].count)
        content[(subIndex)].price = persent_from_summa/content[(subIndex)].count
        if (summOrPercent=='%'){
        return persent_from_summa
        }
        if (summOrPercent=='summ'){
        return summa.toFixed(2);
        }}
    }
  },
  methods: {
    disOptPercent(part, opt){
    var count=0
    part.forEach(function (val){
        if(val.unit=='%'){
            count++
        } 
    })

    if((part.length / count) < 2.5 && opt=='%'){
        return true
    }
},
    toModel(newVal, part){
   partx[part].parts.part_name=newVal.target.innerText
    },
   thousandSeparator(str) {
    return str
    },

    discOfPercent(){
  

var tmpDisc, tmpNetto, tmpTax, tmpTax2
        if(this.butDiscPerc=='%'){
            var add = 0
            partx.forEach((val)=>{
                val.parts.part_content.forEach((sval)=>{
                    if (sval.without==true){
                        add = add + ((sval.count*sval.price/100)*this.discP)
                    }
                })
            })
            this.disc=this.thousandSeparator((this.alltotal(partx)/100)*this.discP-add)
            tmpDisc=(this.alltotal(partx)/100)*this.discP-add
        }else{
            this.disc=this.thousandSeparator(this.discP)
            tmpDisc=this.discP   
        }

        this.netto=this.thousandSeparator(this.alltotal(partx)-tmpDisc)
        tmpNetto=this.alltotal(partx)-tmpDisc


        var addt = 0
        var addt2 = 0
            partx.forEach((val)=>{
                val.parts.part_content.forEach((sval, index)=>{
                if(sval.status=='yes'){
                    if (this.alttax[index]!=true){
                        addt = addt + (sval.count*sval.price)
                    } else{
                        addt2 = addt2 + (sval.count*sval.price)
                    }
                }
                })
            })
  
        this.tax=this.thousandSeparator(addt*(this.taxP/100))
        tmpTax=(addt*(this.taxP/100))

        this.tax2=this.thousandSeparator(addt2*(this.taxP2/100))
     //   tmpTax2=  addt2*(this.taxP2/100)
        tmpTax2=0

        this.brutto=this.thousandSeparator(tmpNetto+tmpTax+tmpTax2)

    },
selectRow(part, subIndex){
if (this.color.indexOf(part+'-'+subIndex) != -1) {
    this.color.splice(this.color.indexOf(part+'-'+subIndex), 1)
} else{
this.color.push(part+'-'+subIndex)
}
},
  move(){    
if(this.color.length!=0){ 
    this.counter=-1
    this.moveToCopy=[]
    this.oldPartx=[]
    this.$refs.move.show()
} else{
    alert('no selected rows')
}
},
moveToCopySelect(event, radio){
var tmpArr=this.tmpArr =[]
this.oldColor.push(JSON.parse(JSON.stringify(this.color)))
this.oldPartx.push(JSON.parse(JSON.stringify(partx)))
var tmpArrCp = JSON.parse(JSON.stringify(partx))
var newColor=[]
this.color.forEach(function(clolorRow){
var partIndex=clolorRow.split('-')
    partx.forEach(function(part, index){
        var temRow = ''
        var other = ''
        if (part.parts.part_name==partIndex[0]){
            temRow = part.parts.part_content[partIndex[1]]
            other = tmpArrCp[index].parts.part_content[partIndex[1]]
            tmpArr.splice(0, 0, other)
            if (radio=='Move') {part.parts.part_content.splice(temRow, 1)}
        }
    })
})

event.forEach(function(eve){
  partx.forEach(function(part){
        if (part.parts.part_name==eve){
            tmpArr.forEach(function(val, index){
                newColor.push(part.parts.part_name+'-'+index)
                part.parts.part_content.unshift(val)
            })
        }
    })
})
this.color=[]
this.color=newColor.slice()
this.counter = this.counter + 1
console.log(this.counter)
},
cancelPartx(indexButton){
console.log(indexButton)
    this.color=[]
    this.moveToCopy=[]
    console.log(this.oldPartx, this.oldColor)
    partx.splice(0, partx.length)
    this.oldPartx[indexButton].forEach(function(val){
        partx.push(val)
    })
    this.color=JSON.parse(JSON.stringify(this.oldColor[indexButton]))
    this.counter = this.counter - 1
},
okMoveToCopy(){
this.$refs.move.hide()
},    
  
  inItemClick(item, index) {
       // console.log(item),
        //this.tmp = item.parts,
        this.tmp.number = item.offer_number,
        this.tmp.date = item.date,
        this.tmp.place = item.place,
        this.tmp.insurance = item.insurance_number,
        this.tmp.work = item.work,
        this.tmp.other = item.other
        },
        inItemClickPrice(item, index) {
        this.toggle.forEach(function (valueToggle) {
            partx.forEach(function (valuePart, index) {
                if(valuePart.parts.part_name+index == valueToggle){

for (var property in valuePart.parts.checkbox_list.flavours) {
valuePart.parts.checkbox_list.flavours[property].push('temp'+valuePart.parts.checkbox_list.flavours[property].length)
}
      valuePart.parts.part_content.push(
                   { //сheckbox:item.checkbox,
                    position_number:item.position_number,
                    description_head:item.description_head,
                    description_work:item.description_work,
                    description_from_price:item.description_from_price,
                    count:item.count,
                    discount:item.discount,
                    price:item.price,
                    status:item.status,
                    summa:item.summa,
                    unit:item.unit,
                    without:item.without,
                    upHere:false,
                    сheckbox:item.сheckbox
                    }); 
                } 
            });
        });
},
    keyupMethod(event){
if (event.keyCode === 113) {
    this.tmouseOver()
  }
  if (event.keyCode === 27) {
      this.mouseOut()
  }
    },

    classRow(arrayColumnOfPart, keyindex){
        var countPercent=-1
        arrayColumnOfPart.part_content.forEach(function(val, index){
          if(arrayColumnOfPart.part_content[index].upHere==true && val.unit=='%'){
                for (var i=0; i <= index; i++) {
                     if (countPercent < index && arrayColumnOfPart.part_content[i].unit == '%'){
                                              countPercent++
                         }
                }  
            }
         })
        if('in'+countPercent==keyindex){
            return 'upHereColumn'
        }
    },
  
    boxDisable(unit, obj, str){
      if(unit=='%'){
        return true
      } else{  
        var dis=0
        this.disable.forEach(function(val){
        var vals=val.split('-')
            if(vals[0] != obj){
                if (vals[1]==str){
                    dis++
                }
            }
        })         
        if (dis!=0){
          return true
        }        
      }
    },
    scheckStatus(){
        partx.forEach((part)=>{
            var obj 
                for (obj in part.parts.checkbox_list.selected){
                    var countStr=0
                    var check=0
                    
                    part.parts.part_content.forEach((val, index)=>{
                        if(val.unit == '%') {
                            countStr++
                        }else{
                            var dis
                            this.disable.forEach(function(dval){
                                dis=dval.split('-')
                               
                                if (index==dis[1]){
                                    check++
                                } 
                            })
                        }
                        if((countStr+check)==part.parts.checkbox_list.flavours[obj].length){
                        var objAls
                        for (objAls in part.parts.checkbox_list.allSelected){
                            if (objAls==obj){
                                var dis1
                                var uncheck=0
                                this.disable.forEach(function(dval1){
                                    dis1=dval1.split('-')
                                   
                                    if (objAls==dis1[0]){
                                        uncheck++
                                    } 
                                })
                                if(uncheck!=0){
                                this.$set(part.parts.checkbox_list.allSelected, objAls, true)
                                }
                            } 
                        }
                    }else{
                        this.$set(part.parts.checkbox_list.allSelected, obj, false)
                        }
                    
                    })
              
                  
                
                }

        })

    },
    box(event, obj, str){
    if (event!=null){
    this.disable.push(obj+'-'+str)} else{this.disable.splice(this.disable.indexOf(obj+'-'+str), 1)}
    this.scheckStatus()
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
               {parts:{part_name: nameofpart.value,

checkbox_list: {
  flavours: {},
    selected: {},
    allSelected: {},
    indeterminate: {}
}, 

             part_content:[]}}
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

//console.log(valuePart.parts.checkbox_list.selected)
                  for (var property in valuePart.parts.checkbox_list.flavours) {
//определить значение и удалить по нему
                      valuePart.parts.checkbox_list.selected[property].splice(valuePart.parts.checkbox_list.selected[property].indexOf(valuePart.parts.checkbox_list.flavours[property][subDel_id]), 1)   
                      valuePart.parts.checkbox_list.flavours[property].splice(subDel_id, 1)
                    }      
                 

            } 
        });
    },
persent(val, index, checkbox_in_table, how_many_rows){
    this.persentCounter=val
    if (val=='%'){
        //почему 3 раза сработала????
        this.add_column_checkbox(checkbox_in_table, how_many_rows)
        
        for (var obj in checkbox_in_table.flavours) {
          }  
    checkbox_in_table.selected[obj].push(checkbox_in_table.flavours[obj][index])

    }
    else {
          for (var obj in checkbox_in_table.flavours) {
             var valCecked = checkbox_in_table.flavours[obj][index]
             if(checkbox_in_table.selected[obj].indexOf(valCecked)!=-1 ){
                this.remove_column_checkbox(checkbox_in_table, obj)
             }
        }
    }
},

remove_column_checkbox(checkbox_in_table, key){
this.$delete(checkbox_in_table.indeterminate, key)
this.$delete(checkbox_in_table.allSelected, key)
this.$delete(checkbox_in_table.flavours, key)
this.$delete(checkbox_in_table.selected, key)
},    
add_column_checkbox(checkbox_in_table, how_many_rows){
var sum_of_property = 0
for (var property in checkbox_in_table.allSelected) {
  sum_of_property += 1
}

var flavour = new Array()
for (var row = 1; row<=how_many_rows; row++) {
  flavour.push('temp'+row)
}

this.$set(checkbox_in_table.allSelected, 'in'+sum_of_property, false)
this.$set(checkbox_in_table.flavours, 'in'+sum_of_property, flavour)
this.$set(checkbox_in_table.indeterminate, 'in'+sum_of_property, false)
this.$set(checkbox_in_table.selected, 'in'+sum_of_property, [])
this.scheckStatus()
},
toggleAll(event, target, model, persent) {

    model.allSelected[target]=event
    if (model.allSelected[target]){
    var obj
          model.flavours[target].forEach( (val, index) => {
           
            if(persent[index].unit!='%'){
                var count = 0
                for (obj in model.allSelected) {
                  if (model.flavours[target][index] == model.selected[obj][model.selected[obj].indexOf(model.flavours[target][index])]) count++
                }
                if (count == 0){
                   
                    model.selected[target].push(model.flavours[target][index])
                    this.box(model.flavours[target][index], target, index)
                }
            } 
        })

    }
    else {
    var obj
         model.flavours[target].forEach( (val, index) => {
            if(persent[index].unit!='%'){
                if(model.selected[target].indexOf(model.flavours[target][index])!=-1){
                model.selected[target].splice(model.selected[target].indexOf(model.flavours[target][index]), 1)
                 this.box(null, target, index)
            }}
        })
    }

              
    }
 },
   
watch: { 
  partx: {
    handler: function(newVal) {
            var result
            var sval
            var separator
            var indexReplace, indexRuslt
            var safeEval = require('safe-eval')
            

        partx.forEach((part, index) => {
        for (var obj in newVal[index].parts.part_content) {
             var tname = 't'+index+'x'+obj
            if(newVal[index].parts.part_content[obj].description_work.indexOf(' ')!=-1) {
            separator = this.$refs[tname][0].quill.getText()
            separator = separator.replace(/\n/g, ' ')
            separator = separator.substring(0, separator.length - 1);
             separator=separator.split(' ')
             separator.splice(-1,1)
             separator.forEach((val)=>{
                if(val.search(/[a-zA-z=]/gim)==-1){
                if(val.search(/[-+*)(/]/gim)>-1){
                if(val.search(/[0-9]/gim)>-1){
                if(/[\d)]/.test(val[val.length-1])){
                 
                try {
                    result= this.thousandSeparator(safeEval(val))
                    } catch(e) {
                    result= '(not valid formula)'
                  }
                sval=val.replace(/([-+*)(/])/gim, '$1&shy;')+'='+result+' '
                indexRuslt = result.length ? result.length : 4
                indexReplace = partx[index].parts.part_content[obj].description_work.indexOf(val)+indexRuslt+6
                this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(partx[index].parts.part_content[obj].description_work.replace(val, sval))
                this.$refs[tname][0].quill.setSelection(indexReplace, 0)
               }
           }
       }
        }
             })
             

            }

      }
 })
    },
    deep: true, 
},

commentOfTable: function (value) {
 
    var result
      var sval
      var separator
      var indexReplace, indexRuslt
      var safeEval = require('safe-eval')

            if(this.commentOfTable.indexOf(' ')!=-1) {
            separator = this.$refs.refCommentOfTable.quill.getText()
            separator = separator.replace(/\n/g, ' ')
            separator = separator.substring(0, separator.length - 1);
             separator=separator.split(' ')
             separator.splice(-1,1)
             separator.forEach((val)=>{
                if(val.search(/[a-zA-z=]/gim)==-1){
                if(val.search(/[-+*)(/]/gim)>-1){
                if(val.search(/[0-9]/gim)>-1){
                if(/[\d)]/.test(val[val.length-1])){
                 
                try {
                    result= this.thousandSeparator(safeEval(val))
                    } catch(e) {
                    result= '(not valid formula)'
                  }
                sval=val.replace(/([-+*)(/])/gim, '$1&shy;')+'='+result+' '
                indexRuslt = result.length ? result.length : 4
                indexReplace = this.commentOfTable.indexOf(val)+indexRuslt+6
                this.$refs.refCommentOfTable.quill.clipboard.dangerouslyPasteHTML(this.commentOfTable.replace(val, sval))
                this.$refs.refCommentOfTable.quill.setSelection(indexReplace, indexReplace)
               }
           }
       }
}
})
}




 }
  },
  //          var endResult
  //          var middleResult
  //          var startResult
  //          var result
  //          var safeEval = require('safe-eval')
  //          if(val.indexOf('= ') + 1) {
  //              endResult=val.split('= ')[0]
  //              middleResult=endResult.split(' ')
  //              startResult=middleResult[middleResult.length-1]
  //              startResult=startResult.replace(/[^-+*)(/=^0-9]/gim,'')
  //                  try {
  //                    result= this.thousandSeparator(safeEval(startResult))
  //                  } catch(e) {
  //                    result= '(not valid formula)'
  //                  }

         
            
//                this.commentOfTable=this.commentOfTable.replace('= ', '='+result+' ');

  //              setTimeout(() => {
    //                if (result=='(not valid formula)') {
      //             this.$refs.refCommentOfTable.$el.selectionStart =endResult.length+1;
       //            this.$refs.refCommentOfTable.$el.selectionEnd =(endResult.length+1)+result.length;
       //            } else{
       //            this.$refs.refCommentOfTable.$el.selectionStart =(endResult.length+1)+result.length;
       //            this.$refs.refCommentOfTable.$el.selectionEnd =(endResult.length+1)+result.length;
       //            }
       //         }, 10);
  //  }



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
  },
  created: function () {

            document.addEventListener('keyup', this.keyupMethod)
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
.v-select .open-indicator::before {
  margin-top: 4px;
  width:  7px ;
  height:  7px;
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
.dropdown-toggle::after {
display: none !important;
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
.withoutborder {
    border-top: 0px !important;
}

.collapsed > .when-opened,
:not(.collapsed) > .when-closed {
  display: none;
}
.withoutPad{
margin: 0px !important;
margin-left: 5px !important;
    margin-top: 4px !important;
}
.withoutborder th, .withoutborder td {
    border-top: 0px !important;
}
.howerRow{
background: #e9ecef;
}
.upHereColumn{
background-color: #007bff !important;
}

.upHereColumn input{
background-color: #007bff !important;
}
/*////////////////////*/



.tposition input, .tdeschead input, .tcount input, .tunit input, .tprice input, .twithout input, .tcalc input{
   /* background-color: rgba(0,0,0,0.8);*/

}

.tnumber{
font-size: 12px;
font-weight:bold;
width:5%;
max-width: 20px;
font-weight:bold;
}
.tposition{ 
font-size: 12px;
font-weight:bold;
width:10%;
}
.tdeschead{
font-size: 12px;
font-weight:bold;
width:32%;
}
.tinfo{
font-size: 12px;
font-weight:bold;
width:5%;
max-width: 20px;
}
.tcount{
font-size: 12px;
font-weight:bold;
width:4%;
}

.tunit{
font-size: 12px;
font-weight:bold;
width:8%;
}
.tprice{
font-size: 12px;
font-weight:bold;
width:8%;
}
.tsumm{
font-size: 12px;
font-weight:bold;
padding-top: 2px;
     overflow: hidden; 
width:9%;
}
.ttotalsumm{
font-size: 12px;
font-weight:bold;
padding-top: 2px;

}
.twithout{
font-size: 12px;
font-weight:bold;
width:6%;
max-width: 25px;
}
.tpercent{
font-size: 12px;
font-weight:bold;
min-width: 5%;
    padding-left: 10px;
    margin-right: 5px;
}                                      
.tcalc{
font-size: 12px;
font-weight:bold;
width:10%;
}
.tdelete{
font-size: 12px;
font-weight:bold;
width:2%;
}
.totalTable{
font-size: 12px;
font-weight:bold;
}
input{
    padding: 2px !important;
}

.ainput{
      text-align: center !important;
}
.rinput{
    text-align: right !important;
}
.cinput{
    text-align: center !important;
}
.greenrow .form-row{
    background-color: #c8e6c9;
}

@import url(//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css);
.ccbox label{
margin-top: -3px;
width: 15px;
text-align: left;
}
.ccbox input[type=checkbox] { display:none; } /* to hide the checkbox itself */
.ccbox input[type=checkbox] + label:before {
  font-family: FontAwesome;
}
.ccbox input[type=checkbox] + label:before {
content: "\f096";
font-size: 14px;
font-weight: 100;
} /* unchecked icon */
.ccbox input[type=checkbox]:checked + label:before {
content: "\f046";
font-size: 14px;
font-weight: 100;
} /* checked icon */
.calttax{
    text-decoration: underline;
}
.quillWrapper .ql-snow.ql-toolbar {
padding-top: 0px !important;
height: 30px !important;
}

.ql-snow.ql-toolbar button svg {
    height: 13px !important;
}
</style>