<!--
* Tencent is pleased to support the open source community by making
* 蓝鲸智云PaaS平台 (BlueKing PaaS) available.
*
* Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
*
* 蓝鲸智云PaaS平台 (BlueKing PaaS) is licensed under the MIT License.
*
* License for 蓝鲸智云PaaS平台 (BlueKing PaaS):
*
* ---------------------------------------------------
* Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
* documentation files (the "Software"), to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
* to permit persons to whom the Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of
* the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
* THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
* CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
* IN THE SOFTWARE.
-->

<template>
  <div
    class="step-storage"
    v-bkloading="{ isLoading: basicLoading }"
  >
    <bk-form
      ref="validateForm"
      :label-width="150"
      :model="formData"
      data-test-id="storage_form_storageBox"
    >
      <div class="add-collection-title">{{ $t('集群选择') }}</div>
      <cluster-table
        :is-change-select.sync="isChangeSelect"
        :storage-cluster-id.sync="formData.storage_cluster_id"
        :table-list="clusterList"
      />

      <cluster-table
        style="margin-top: 20px"
        :is-change-select.sync="isChangeSelect"
        :storage-cluster-id.sync="formData.storage_cluster_id"
        :table-list="exclusiveList"
        table-type="exclusive"
      />

      <div class="add-collection-title">{{ $t('存储信息') }}</div>
      <!-- 存储索索引名 -->
      <div class="form-div mt">
        <bk-form-item
          class="form-inline-div"
          :label="$t('索引名')"
          :property="'table_id'"
        >
          <!-- <div class="prefix">{{formData.table_id_prefix}}</div> -->
          <bk-input
            style="width: 320px"
            v-model="formData.table_id"
            :placeholder="$t('英文或者数字，5～50长度')"
            disabled
          >
            <template #prepend>
              <div class="group-text">{{ formData.table_id_prefix }}</div>
            </template>
          </bk-input>
        </bk-form-item>
        <!-- <div class="tips">{{ $t('以业务ID+bklog_开头,补充字母、数字或下划线，5~50长度') }}</div> -->
      </div>
      <!-- 过期时间 -->
      <bk-form-item :label="$t('过期时间')">
        <bk-select
          style="width: 320px"
          v-model="formData.retention"
          :clearable="false"
          data-test-id="storageBox_select_selectExpiration"
        >
          <template #trigger>
            <div class="bk-select-name">
              {{ formData.retention + $t('天') }}
            </div>
          </template>
          <template>
            <bk-option
              v-for="(option, index) in retentionDaysList"
              :id="option.id"
              :key="index"
              :name="option.name"
            ></bk-option>
          </template>
          <template #extension>
            <div style="padding: 8px 0">
              <bk-input
                v-model="customRetentionDay"
                :placeholder="$t('输入自定义天数，按 Enter 确认')"
                :show-controls="false"
                data-test-id="storageBox_input_customDayNumber"
                size="small"
                type="number"
                @enter="enterCustomDay($event, 'retention')"
              ></bk-input>
            </div>
          </template>
        </bk-select>
      </bk-form-item>
      <!-- 热数据\冷热集群存储期限 -->
      <bk-form-item
        v-if="selectedStorageCluster.enable_hot_warm"
        class="hot-data-form-item"
        :label="$t('热数据天数')"
      >
        <bk-select
          style="width: 320px"
          v-model="formData.allocation_min_days"
          :clearable="false"
          :disabled="!selectedStorageCluster.enable_hot_warm"
          data-test-id="storageBox_select_selectHotData"
        >
        <template #trigger>
            <div class="bk-select-name">
              {{ formData.allocation_min_days + $t('天') }}
            </div>
          </template>
          <template>
            <bk-option
              v-for="(option, index) in hotDataDaysList"
              :id="option.id"
              :key="index"
              :name="option.name"
            ></bk-option>
          </template>
          <template #extension>
            <div style="padding: 8px 0">
              <bk-input
                v-model="customHotDataDay"
                :placeholder="$t('输入自定义天数，按 Enter 确认')"
                :show-controls="false"
                data-test-id="storageBox_input_customize"
                size="small"
                type="number"
                @enter="enterCustomDay($event, 'hot')"
              ></bk-input>
            </div>
          </template>
        </bk-select>
        <span
          v-if="!selectedStorageCluster.enable_hot_warm"
          class="disable-tips"
        >
          {{ $t('该集群未开启热数据设置') }}
          <a
            href="javascript:void(0);"
            @click="jumpToEsAccess"
            >{{ $t('前往ES源进行设置') }}</a
          >
        </span>
      </bk-form-item>
      <!-- 副本数 -->
      <bk-form-item
        ext-cls="number-input"
        :label="$t('副本数')"
        :property="'storage_replies'"
        :rules="rules.storage_replies"
      >
        <bk-input
          class="copy-number-input"
          v-model="formData.storage_replies"
          :clearable="false"
          :min="0"
          :precision="0"
          :show-controls="true"
          type="number"
          @blur="changeCopyNumber"
        ></bk-input>
      </bk-form-item>
      <!-- 分片数 -->
      <bk-form-item
        ext-cls="number-input"
        :label="$t('分片数')"
        :property="'es_shards'"
        :rules="rules.es_shards"
      >
        <bk-input
          class="copy-number-input"
          v-model="formData.es_shards"
          :clearable="false"
          :min="1"
          :precision="0"
          :show-controls="true"
          type="number"
          @blur="changeShardsNumber"
        ></bk-input>
      </bk-form-item>
      <div
        v-if="isCanUseAssessment"
        class="capacity-assessment"
      >
        <div
          class="button-text"
          @click="isShowAssessment = !isShowAssessment"
        >
          <span>{{ $t('容量评估') }}</span>
          <span :class="['bk-icon', 'icon-angle-double-down', isShowAssessment && 'is-active']"></span>
        </div>
        <div
          v-if="isForcedFillAssessment"
          class="capacity-message"
        >
          <span class="bk-icon icon-info"></span>
          <span style="font-size: 12px">{{ $t('当前主机数较多，请进行容量评估') }}</span>
        </div>
      </div>
      <div v-show="isShowAssessment && isCanUseAssessment">
        <div class="capacity-illustrate">
          <p class="illustrate-title">{{ $t('容量说明') }}</p>
          <p>{{ $t('容量计算公式：单机日志增量主机数量存储转化率分片数（日志保留天数 + 1）') }}</p>
          <p>{{ $t('存储转化率（1.5）：即原始日志增加日志采集元数据并存储到ES到实际占有的空间') }}</p>
          <p>
            {{
              $t('分片数（{x}）：1个主分片+{n}个副本数，避免节点故障导致数据丢失', {
                x: formData.storage_replies * 1 + 1,
                n: formData.storage_replies,
              })
            }}
          </p>
        </div>

        <bk-form-item :label="$t('每日单台日志量')">
          <div class="capacity-message">
            <bk-input
              class="capacity-input"
              v-model="formData.assessment_config.log_assessment"
              :min="0.1"
              type="number"
            >
            </bk-input>
            <div class="unit-container">G</div>
            <span
              class="right"
              v-bk-tooltips.right="$t('基于单台最大的日志存储量粗略评估')"
            >
              <i class="bk-icon icon-info"></i>
            </span>
          </div>
        </bk-form-item>

        <div class="need-approval">
          <bk-checkbox
            v-model="formData.assessment_config.need_approval"
            :disabled="isForcedFillAssessment"
          >
            {{ $t('需要审批') }}
          </bk-checkbox>
          <bk-alert
            style="width: 607px"
            :show-icon="false"
            type="warning"
          >
            <template #title>
              <div class="approval-alert">
                <span class="bk-icon icon-exclamation-circle"></span>
                <p>{{ $t('勾选需要审批后需等待审批通过后，才会继续进行存储流程') }}</p>
              </div>
            </template>
          </bk-alert>
        </div>

        <bk-form-item :label="$t('审批人')">
          <span class="approver">{{ $t('集群负责人') }}（ {{ getApprover }} ）</span>
        </bk-form-item>
      </div>
      <!-- 查看权限 -->
      <!-- <bk-form-item
        v-if="accessUserManage"
        :label="$t('查看权限')"
        required
        :property="'view_roles'"
        :rules="rules.view_roles"
        style="width: 435px;">
        <bk-select
          style="width: 320px;"
          data-test-id="storageBox_select_viewPermission"
          v-model="formData.view_roles"
          searchable
          multiple
          :placeholder="$t('请选择')"
          show-select-all>
          <bk-option
            v-for="(role, index) in roleList"
            :key="index"
            :id="role.group_id"
            :name="role.group_name">
          </bk-option>
        </bk-select>
      </bk-form-item> -->
      <bk-form-item class="operate-container">
        <template v-if="!isFinishCreateStep">
          <bk-button
            class="mr10"
            :disabled="isLoading"
            :title="$t('上一步')"
            data-test-id="storageBox_button_previousPage"
            theme="default"
            @click="prevHandler"
          >
            {{ $t('上一步') }}
          </bk-button>
          <bk-button
            class="mr10"
            :disabled="!collectProject"
            :loading="isLoading"
            data-test-id="storageBox_button_nextPage"
            theme="primary"
            @click.stop.prevent="finish()"
          >
            {{ $t('下一步') }}
          </bk-button>
        </template>
        <template v-else>
          <bk-button
            class="mr10"
            :disabled="!collectProject"
            :loading="isLoading"
            theme="primary"
            @click.stop.prevent="finish()"
          >
            {{ $t('保存') }}
          </bk-button>
        </template>
        <bk-button
          theme="default"
          @click="cancel"
        >
          {{ $t('取消') }}
        </bk-button>
      </bk-form-item>
    </bk-form>
  </div>
</template>

<script>
  import { projectManages, deepEqual } from '@/common/util';
  import storageMixin from '@/mixins/storage-mixin';
  import { mapGetters } from 'vuex';

  import ClusterTable from './components/cluster-table';

  export default {
    components: {
      ClusterTable,
    },
    mixins: [storageMixin],
    props: {
      operateType: String,
      curStep: {
        type: Number,
        default: 1,
      },
      collectorId: String,
      /** 是否已走过一次完整步骤，编辑状态显示不同的操作按钮 */
      isFinishCreateStep: {
        type: Boolean,
        require: true,
      },
    },
    data() {
      return {
        isItsm: window.FEATURE_TOGGLE.collect_itsm === 'on',
        HOST_COUNT: window.ASSESSMEN_HOST_COUNT,
        refresh: false,

        isLoading: false,
        basicLoading: true,
        isUnmodifiable: false,
        isUnmodfyIndexName: false,
        // roleList: [],
        fieldType: '',
        deletedVisible: true,
        copysText: {},
        jsonText: {},
        defaultSettings: {
          isShow: false,
        },
        logOriginal: '',
        params: {
          // 此处为可以变动的数据，如果调试成功，则将此条件保存至formData，保存时还需要对比此处与formData是否有差异
          etl_config: 'bk_log_text',
          etl_params: {
            separator_regexp: '',
            separator: '',
          },
        },
        formData: {
          // 最后一次正确的结果，保存以此数据为准
          table_id: '',
          etl_config: 'bk_log_text',
          etl_params: {
            retain_original_text: true,
            retain_extra_json: false,
            separator_regexp: '',
            separator: '',
            enable_retain_content: true, // 保留失败日志
            path_regexp: '', // 采集路径分割的正则
            // separator_field_list: '',
            metadata_fields: [],
          },
          fields: [],
          view_roles: [],
          retention: '',
          storage_replies: 0,
          es_shards: 0,
          allocation_min_days: '0',
          storage_cluster_id: '',
          assessment_config: {
            log_assessment: '',
            need_approval: false,
            approvals: [],
          },
        },
        selectedStorageCluster: {}, // 选择的es集群
        retentionDaysList: [], // 过期天数列表
        customRetentionDay: '', // 自定义过期天数
        hotDataDaysList: [], // 冷热集群存储期限列表
        customHotDataDay: '', // 自定义冷热集群存储期限天数
        rules: {
          cluster_id: [
            {
              validator(val) {
                return val !== '';
              },
              trigger: 'change',
            },
          ],
          view_roles: [
            {
              validator(val) {
                return val.length >= 1;
              },
              trigger: 'change',
            },
          ],
          storage_replies: [
            {
              validator: this.checkStorageReplies,
              message: () => window.mainComponent.$t('最大自定义副本数为: {n}', { n: this.replicasMax }),
              trigger: 'blur',
            },
            {
              validator: this.checkStorageReplies,
              message: () => window.mainComponent.$t('最大自定义副本数为: {n}', { n: this.replicasMax }),
              trigger: 'change',
            },
          ],
          es_shards: [
            {
              validator: this.checkEsShards,
              message: () => window.mainComponent.$t('最大自定义分片数为: {n}', { n: this.shardsMax }),
              trigger: 'blur',
            },
            {
              validator: this.checkEsShards,
              message: () => window.mainComponent.$t('最大自定义分片数为: {n}', { n: this.shardsMax }),
              trigger: 'change',
            },
          ],
        },
        storage_capacity: '',
        tips_storage: [],
        tip_storage: [],
        storageList: [],
        clusterList: [], // 共享集群
        exclusiveList: [], // 独享集群
        dialogVisible: false,
        rowTemplate: {
          alias_name: '',
          description: '',
          field_type: '',
          is_analyzed: false,
          is_built_in: false,
          is_delete: false,
          is_dimension: false,
          is_time: false,
          value: '',
          option: {
            time_format: '',
            time_zone: '',
          },
        },
        stashCleanConf: null, // 清洗缓存,
        isShowAssessment: false,
        isChangeSelect: false,
        hostNumber: 0,
        replicasMax: 7,
        shardsMax: 7,
        isForcedFillAssessment: false, // 是否必须容量评估
        editStorageClusterID: null, // 存储页进入时判断是否有选择过存储集群
        editComparedData: {},
      };
    },
    computed: {
      ...mapGetters({
        bkBizId: 'bkBizId',
        spaceUid: 'spaceUid',
        curCollect: 'collect/curCollect',
        globalsData: 'globals/globalsData',
        accessUserManage: 'accessUserManage',
        isShowMaskingTemplate: 'isShowMaskingTemplate',
        exportCollectObj: 'collect/exportCollectObj',
      }),
      collectProject() {
        return projectManages(this.$store.state.topMenu, 'collection-item');
      },
      defaultRetention() {
        const { storage_duration_time } = this.globalsData;

        return storage_duration_time?.filter(item => item.default === true)[0].id;
      },
      isCanUseAssessment() {
        /**
         * itsm开启时, 当前选择的集群容量评估开启时
         * isChangeSelect 当前步骤非新增,且进行集群切换满足上面条件则展示容量评估
         */
        return this.isItsm && this.selectedStorageCluster.enable_assessment && this.isChangeSelect;
      },
      getApprover() {
        if (this.isCanUseAssessment) {
          // eslint-disable-next-line vue/no-side-effects-in-computed-properties
          this.formData.assessment_config.approvals = this.selectedStorageCluster?.admin || [];
          return this.selectedStorageCluster?.admin.join(', ') || '';
        }
        return '';
      },
    },
    async mounted() {
      this.operateType === 'add' && (this.isChangeSelect = true);
      await this.getStorage();
      await this.getCleanStash();
      this.getDetail();
      this.exportStorage();
    },
    created() {
      this.curCollect.environment !== 'container' && this.getHostNumber();
    },
    methods: {
      // 获取采集项清洗基础配置缓存 用于存储入库提交
      async getCleanStash() {
        try {
          const res = await this.$http.request('clean/getCleanStash', {
            params: {
              collector_config_id: this.curCollect.collector_config_id,
            },
          });
          if (res.data) this.stashCleanConf = res.data;
        } catch (error) {}
      },
      // 存储入库
      fieldCollection(callback) {
        const data = this.getSubmitData();

        this.isLoading = true;
        this.$http
          .request('collect/fieldCollection', {
            params: {
              collector_config_id: this.curCollect.collector_config_id,
            },
            data,
          })
          .then(res => {
            if (res.code === 0) {
              // this.storageList = res.data
              // this.formData.storage_cluster_id = this.storageList[0].storage_cluster_id
              if (res.data) {
                this.$store.commit('collect/updateCurCollect', Object.assign({}, this.formData, data, res.data));
                this.$emit('change-index-set-id', res.data.index_set_id || '');
              }
              if (data.need_assessment && data.assessment_config.need_approval) {
                this.$emit('set-assessment-item', {
                  iframe_ticket_url: res.data.ticket_url,
                  itsm_ticket_status: 'applying',
                });
              } else {
                this.$emit('set-assessment-item', {});
              }
              if (this.isFinishCreateStep) {
                this.messageSuccess(this.$t('保存成功'));
                if (callback) {
                  this.$emit('reset-cur-collect-val');
                  callback(true);
                  return;
                }
                this.$emit('change-submit', true);
                this.$emit('step-change', 'back');
                return;
              }
              // 只有在不展示日志脱敏的情况下才改变保存状态
              if (!this.isShowMaskingTemplate) this.$emit('change-submit', true);
              this.$emit('step-change');
            }
          })
          .catch(() => callback?.(false))
          .finally(() => {
            this.isLoading = false;
          });
      },
      /** 导航切换提交函数 */
      stepSubmitFun(callback) {
        this.finish(callback);
      },
      // 完成按钮
      finish(callback) {
        const isCanSubmit = this.getSubmitAuthority();
        if (!isCanSubmit) {
          callback?.(false);
          return;
        }
        const promises = [this.checkStore()];
        Promise.all(promises).then(
          () => {
            this.fieldCollection(callback);
          },
          validator => {
            console.warn('保存失败', validator);
          },
        );
      },
      // 存储校验
      checkStore() {
        return new Promise((resolve, reject) => {
          // if (!this.isUnmodifiable) {

          // } else {
          //   resolve();
          // }
          this.$refs.validateForm
            .validate()
            .then(validator => {
              resolve(validator);
            })
            .catch(err => {
              console.warn('存储校验错误');
              reject(err);
            });
        });
      },
      prevHandler() {
        this.$emit('step-change', this.curStep - 1);
      },
      // 获取详情
      getDetail() {
        const tsStorageId = this.formData.storage_cluster_id;
        const {
          table_id,
          storage_cluster_id,
          retention,
          storage_replies,
          storage_shards_nums: storageShardsNums,
          allocation_min_days,
          table_id_prefix,
          view_roles,
          etl_config,
          etl_params,
          fields,
          collector_config_name_en,
        } = this.curCollect;
        const option = { time_zone: '', time_format: '' };
        const copyFields = fields ? JSON.parse(JSON.stringify(fields)) : [];
        copyFields.forEach(row => {
          row.value = '';
          if (row.is_delete) {
            const copyRow = Object.assign(
              JSON.parse(JSON.stringify(this.rowTemplate)),
              JSON.parse(JSON.stringify(row)),
            );
            Object.assign(row, copyRow);
          }
          if (row.option) {
            row.option = Object.assign({}, option, row.option || {});
          } else {
            row.option = Object.assign({}, option);
          }
        });
        /* eslint-disable */
        this.params.etl_config = etl_config;
        Object.assign(this.params.etl_params, {
          separator_regexp: etl_params.separator_regexp || '',
          separator: etl_params.separator || '',
        });
        this.isUnmodifiable = !!(table_id || storage_cluster_id);
        this.isUnmodfyIndexName = !!(table_id || storage_cluster_id || collector_config_name_en);
        this.fieldType = etl_config || 'bk_log_text';
        let default_exclusive_cluster_id;
        if (!storage_cluster_id && this.exclusiveList.length) {
          // 新增时若有业务独享集群则直接赋值独享集群列表第一条id
          this.isChangeSelect = true; // 不提示切换集群dialog
          default_exclusive_cluster_id = this.exclusiveList[0].storage_cluster_id;
        }
        // this.switcher = etl_config ? etl_config !== 'bk_log_text' : false
        /* eslint-enable */
        Object.assign(this.formData, {
          table_id: table_id ? table_id : collector_config_name_en ? collector_config_name_en : '',

          storage_cluster_id: default_exclusive_cluster_id ? default_exclusive_cluster_id : storage_cluster_id,
          es_shards: storageShardsNums,
          table_id_prefix,
          etl_config: this.fieldType,
          etl_params: Object.assign(
            {
              retain_original_text: true,
              retain_extra_json: false,
              original_text_is_case_sensitive: false,
              original_text_tokenize_on_chars: '',
              separator_regexp: '',
              separator: '',
              // separator_field_list: ''
            },

            etl_params ? JSON.parse(JSON.stringify(etl_params)) : {},
          ),
          fields: copyFields.filter(item => !item.is_built_in),
          retention: retention ? `${retention}` : this.defaultRetention,
          storage_replies,

          allocation_min_days: allocation_min_days ? `${allocation_min_days}` : '0',
          view_roles,
        });

        if (this.stashCleanConf) {
          // 缓存清洗配置
          Object.assign(this.formData, {
            etl_config: this.stashCleanConf.clean_type,
            etl_params: this.stashCleanConf.etl_params,
            fields: this.stashCleanConf.etl_fields,
          });
        }

        this.editStorageClusterID = storage_cluster_id;
        this.formData.storage_cluster_id =
          this.formData.storage_cluster_id === null ? tsStorageId : this.formData.storage_cluster_id;
        this.basicLoading = false;
      },
      cancel() {
        if (this.isFinishCreateStep) {
          this.$emit('change-submit', true);
        }
        let routeName;
        const { backRoute, ...reset } = this.$route.query;
        if (backRoute) {
          routeName = backRoute;
        } else {
          routeName = 'collection-item';
        }
        this.$router.push({
          name: routeName,
          query: {
            ...reset,
            spaceUid: this.$store.state.spaceUid,
          },
        });
      },
      /**
       * @desc: 获取主机数数量 若主机数大于assessment_host_count则显示容量评估
       */
      getHostNumber() {
        const curTaskIdList = new Set();
        this.curCollect.task_id_list.forEach(id => curTaskIdList.add(id));
        const params = {
          collector_config_id: this.curCollect.collector_config_id,
        };
        this.$http
          .request('collect/getIssuedClusterList', {
            params,
            query: { task_id_list: [...curTaskIdList.keys()].join(',') },
          })
          .then(res => {
            const data = res.data.contents;
            let hostLength = 0;
            data.forEach(cluster => {
              hostLength += cluster.child.length;
            });
            // 这里获取主机总数量赋值并与HOST_COUNT比较如果主机数量大于最大值则必填容量评估内容
            const isOverHost = hostLength > Number(this.HOST_COUNT);
            this.hostNumber = hostLength;
            this.isShowAssessment = isOverHost;
            this.isForcedFillAssessment = isOverHost;
            this.formData.assessment_config.need_approval = isOverHost;
          })
          .catch(() => {
            this.hostNumber = 0;
            this.isForcedFillAssessment = false;
            this.formData.assessment_config.need_approval = false;
          });
      },
      getSubmitAuthority() {
        /**
         * 当前未选择集群 提示
         * 主机数量 >= assessment_host_count 强制审批 提示
         */
        const { storage_cluster_id: clusterID, assessment_config: assessmentConfig } = this.formData;
        const isNotSelectedID = clusterID === '';
        const isNotFillLog =
          this.isForcedFillAssessment && this.isCanUseAssessment && assessmentConfig.log_assessment === '';
        if (isNotSelectedID || isNotFillLog) {
          const message = isNotSelectedID ? this.$t('请选择集群') : this.$t('请填写容量评估的每日单台日志量');
          this.$bkMessage({
            theme: 'error',
            message,
          });
          return false;
        }
        return true;
      },
      getNeedAssessmentStatus() {
        const {
          assessment_config: { log_assessment: logAssessment, need_approval: needApproval },
        } = this.formData;
        return this.isCanUseAssessment && (logAssessment !== '' || needApproval);
      },
      /** 判断提交信息是否有更改过值 */
      getIsUpdateSubmitValue() {
        // 如果还在初始化的时候快速切换其他导航则直接跳转 不进行数据修改判断
        if (this.basicLoading) return false;
        const params = this.getSubmitData();
        return !deepEqual(this.editComparedData, params);
      },
      getSubmitData() {
        const {
          etl_config,
          table_id,
          storage_cluster_id,
          retention,
          storage_replies,
          es_shards,
          allocation_min_days: allMinDays,
          view_roles,
          fields,
          etl_params: etlParams,
          assessment_config: assessmentConfig,
        } = this.formData;
        const isNeedAssessment = this.getNeedAssessmentStatus();
        const isOpenHotWarm = this.selectedStorageCluster.enable_hot_warm;

        etlParams.metadata_fields =
          etlParams?.metadata_fields?.map(item => {
            item.metadata_type = 'path';
            return item;
          }) ?? [];

        const data = {
          etl_config,
          table_id,
          storage_cluster_id,
          retention: Number(retention),
          storage_replies: Number(storage_replies),
          es_shards: Number(es_shards),
          allocation_min_days: isOpenHotWarm ? Number(allMinDays) : 0,
          view_roles,
          etl_params: {
            retain_original_text: etlParams.retain_original_text,
            retain_extra_json: etlParams.retain_extra_json ?? false,
            original_text_is_case_sensitive: etlParams.original_text_is_case_sensitive ?? false,
            original_text_tokenize_on_chars: etlParams.original_text_tokenize_on_chars ?? '',
            separator_regexp: etlParams.separator === 'bk_log_regexp' ? etlParams.separator_regexp : '',
            separator: etlParams.separator,
            enable_retain_content: etlParams.enable_retain_content,
            record_parse_failure: etlParams.enable_retain_content,
            path_regexp: etlParams.path_regexp,
            metadata_fields: etlParams.metadata_fields,
          },
          fields,
          assessment_config: {
            log_assessment: `${assessmentConfig.log_assessment}G`,
            need_approval: assessmentConfig.need_approval,
            approvals: assessmentConfig.approvals,
          },
          need_assessment: isNeedAssessment,
        };
        !isNeedAssessment && delete data.assessment_config;
        /* eslint-disable */
        if (etl_config !== 'bk_log_text') {
          const payload = {
            retain_original_text: etlParams.retain_original_text,
            retain_extra_json: etlParams.retain_extra_json ?? false,
            original_text_is_case_sensitive: etlParams.original_text_is_case_sensitive ?? false,
            original_text_tokenize_on_chars: etlParams.original_text_tokenize_on_chars ?? '',
            enable_retain_content: etlParams.enable_retain_content,
            record_parse_failure: etlParams.enable_retain_content,
            path_regexp: etlParams.path_regexp,
          };
          if (etl_config === 'bk_log_delimiter') {
            payload.separator = etlParams.separator;
          }
          if (etl_config === 'bk_log_regexp') {
            payload.separator_regexp = etlParams.separator_regexp;
          }
          data.etl_params = payload;
        }
        data.alias_settings = data.fields
          .filter(item => item.query_alias)
          .map(item => {
            return {
              field_name: item.alias_name || item.field_name,
              query_alias: item.query_alias,
              path_type: item.field_type,
            };
          });
        return data;
      },
      checkStorageReplies() {
        return this.formData.storage_replies <= this.replicasMax;
      },
      checkEsShards() {
        return this.formData.es_shards <= this.shardsMax;
      },
      exportStorage() {
        const { syncType, collect } = this.exportCollectObj;
        // 必须是有存储集群的值，而不是未完成的才可以采集配置导入
        const isSyncExport = syncType.includes('storage_config') && !!collect.storage_cluster_id;
        // 这里分两步赋值时因为mixins里有个watch storage_cluster_id的监听函数，会修改其他值
        if (isSyncExport) {
          if (this.storageList.some(item => item.storage_cluster_id === collect.storage_cluster_id)) {
            this.formData.storage_cluster_id = collect.storage_cluster_id;
          } else {
            this.formData.storage_cluster_id = '';
            this.$bkInfo({
              type: 'warning',
              title: this.$t('导入的集群已被删除，请手动选择集群。'),
            });
          }
        }
        this.$nextTick(() => {
          if (isSyncExport) {
            const { retention, storage_replies, storage_shards_nums } = collect;
            Object.assign(this.formData, {
              storage_replies,
              es_shards: storage_shards_nums,
              retention,
            });
          }
          this.editComparedData = this.getSubmitData();
        });
      },
    },
  };
</script>

<style lang="scss">
  @import '@/scss/mixins/clearfix';
  @import '@/scss/storage.scss';
  @import '@/scss/mixins/flex.scss';

  /* stylelint-disable no-descending-specificity */
  .step-storage {
    position: relative;
    min-width: 950px;
    max-height: 100%;
    padding: 0 42px 42px;
    overflow: auto;

    .bk-label {
      font-size: 12px;
    }

    .tips {
      margin-left: 8px;
      font-size: 12px;
      line-height: 32px;
      color: #aeb0b7;
    }

    .form-div {
      display: flex;
      margin: 20px 0;

      .form-inline-div {
        white-space: nowrap;

        .bk-form-content {
          display: flex;
          flex-wrap: nowrap;
        }
      }

      .prefix {
        min-width: 80px;
        margin-right: 8px;
        font-size: 14px;
        line-height: 32px;
        color: #858790;
        text-align: right;
      }
    }

    .add-collection-title {
      width: 100%;
      padding-bottom: 10px;
      margin: 30px 0 20px 0;
      font-size: 14px;
      font-weight: 600;
      color: #63656e;
      border-bottom: 1px solid #dcdee5;
    }

    .capacity-assessment {
      margin: 20px 0;
      font-size: 14px;

      @include flex-align;

      .capacity-message {
        margin-left: 20px;
        color: #63656e;
      }

      .icon-angle-double-down {
        font-size: 24px;

        &.is-active {
          transform: rotateZ(180deg) translateY(-2px);
        }
      }

      .button-text {
        @include flex-align;
      }
    }

    .capacity-illustrate {
      height: 104px;
      padding: 12px 20px;
      margin-bottom: 20px;
      background: #fafbfd;
      border: 1px solid #dcdee5;
      border-radius: 2px;

      .illustrate-title {
        font-weight: 700;
      }

      p {
        margin-bottom: 4px;
        font-size: 12px;
        color: #63656e;
      }
    }

    .capacity-message {
      display: flex;
      align-items: center;

      .capacity-input {
        width: 320px;
      }

      .unit-container {
        width: 40px;
        margin: 1px 0 0 -1px;
        margin-right: 8px;
        color: #63656e;
        text-align: center;
        background: #f2f4f8;
        border: 1px solid #c4c6cc;
      }

      .right {
        color: #63656e;
      }
    }

    .need-approval {
      margin: 12px 0 12px 116px;

      @include flex-align;

      .bk-checkbox-text {
        margin-right: 12px;
        font-size: 12px;
      }

      .approval-alert {
        display: flex;
        align-items: center;
      }

      .icon-exclamation-circle {
        margin-right: 8px;
        font-size: 16px;
        color: #ff9c01;
      }
    }

    .approver {
      font-size: 12px;
      color: #313238;
    }

    .operate-container {
      margin-top: 32px;
      transform: translateX(-115px);
    }
  }
</style>
