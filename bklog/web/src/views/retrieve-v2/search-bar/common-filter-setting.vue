<template>
  <bk-popover
    ref="fieldsSettingPopperRef"
    animation="slide-toggle"
    placement="bottom"
    theme="light bk-select-dropdown"
    trigger="click"
    class="common-filter-popper"
    :on-show="handlePopoverShow"
    :tippy-options="tippyOptions"
  >
    <slot name="trigger">
      <div class="operation-icon">
        <span :class="['bklog-icon bklog-log-setting']"></span>
        设置筛选
      </div>
    </slot>
    <template #content>
      <div class="bklog-common-field-filter fields-container">
        <div class="fields-list-container">
          <div class="total-fields-list">
            <div class="title">
              <span>{{ $t('待选列表') + '(' + toSelectLength + ')' }}</span>
              <span
                class="text-action add-all"
                @click="addAllField"
                >{{ $t('全部添加') }}</span
              >
            </div>
            <div style=" height: 40px;padding: 4px 8px">
              <bk-input
                behavior="simplicity"
                left-icon="bk-icon icon-search"
                v-model="searchKeyword"
                :placeholder="$t('请输入关键字')"
                :clearable="true"
              ></bk-input>
            </div>
            <ul class="select-list">
              <li
                v-for="item in shadowTotal"
                style="cursor: pointer"
                class="select-item"
                :key="item.field_name"
                @click="addField(item)"
                v-bk-overflow-tips="{ content: `${item.query_alias || item.field_name}(${item.field_name})` }"
              >
                <span
                  :style="{ backgroundColor: item.is_full_text ? false : getFieldIconColor(item.field_type) }"
                  :class="[item.is_full_text ? 'full-text' : getFieldIcon(item.field_type), 'field-type-icon']"
                >
                </span>
                <span class="field-alias">{{ item.query_alias || item.field_alias || item.field_name }}</span>
                <span class="field-name">({{ item.field_name }})</span>
                <span class="icon bklog-icon bklog-filled-right-arrow"></span>
              </li>
            </ul>
          </div>
          <div class="sort-icon">
            <span class="icon bklog-icon bklog-double-arrow"></span>
          </div>
          <div class="visible-fields-list">
            <div class="title">
              <span>{{ $t('常驻筛选') + '(' + shadowVisible.length + ')' }}</span>
              <span
                class="icon bklog-icon bklog-info-fill"
                v-bk-tooltips="$t('支持拖拽更改顺序，从上向下对应列表列从左到右顺序')"
              ></span>
              <span
                class="clear-all text-action"
                @click="deleteAllField"
                >{{ $t('清空') }}</span
              >
            </div>
            <vue-draggable
              v-bind="dragOptions"
              class="select-list"
              v-model="shadowVisible"
            >
              <transition-group>
                <li
                  v-for="(item, index) in shadowVisible"
                  class="select-item"
                  :key="item.field_name"
                  v-bk-overflow-tips="{ content: `${item.query_alias || item.field_name}(${item.field_name})` }"
                >
                  <span class="icon bklog-icon bklog-drag-dots"></span>
                  <span
                    :style="{ backgroundColor: item.is_full_text ? false : getFieldIconColor(item.field_type) }"
                    :class="[item.is_full_text ? 'full-text' : getFieldIcon(item.field_type), 'field-type-icon']"
                  >
                  </span>
                  <span class="field-alias">{{ item.query_alias || item.field_name }}</span>
                  <span class="field-name">({{ item.field_name }})</span>
                  <span
                    class="bk-icon icon-close-circle-shape delete"
                    @click="deleteField(item, index)"
                  ></span>
                </li>
              </transition-group>
            </vue-draggable>
          </div>
        </div>
      </div>
      <div class="bklog-common-field-filter fields-button-container">
        <bk-button
          class="mr10"
          :theme="'primary'"
          :loading="isLoading"
          type="submit"
          @click="confirmModifyFields"
        >
          {{ $t('保存') }}
        </bk-button>
        <bk-button
          :theme="'default'"
          type="submit"
          @click="cancelModifyFields"
        >
          {{ $t('取消') }}
        </bk-button>
      </div>
    </template>
  </bk-popover>
</template>
<script setup>
  import { ref, computed, watch, set } from 'vue';
  import useStore from '@/hooks/use-store';
  import useLocale from '@/hooks/use-locale';

  import VueDraggable from 'vuedraggable';
  import { excludesFields } from './const.common';
  import { getRegExp } from '@/common/util';

  // 获取 store
  const store = useStore();
  const { $t } = useLocale();
  const searchKeyword = ref('');
  const tippyOptions = {
    offset: '0, 4',
  };

  // 定义响应式数据
  const isLoading = ref(false);
  const fieldList = computed(() => {
    return store.state.indexFieldInfo.fields;
  });

  const filterFieldsList = computed(() => {
    if (Array.isArray(store.state.retrieve.catchFieldCustomConfig?.filterSetting)) {
      return store.state.retrieve.catchFieldCustomConfig?.filterSetting ?? [];
    }

    return [];
  });

  const shadowTotal = computed(() => {
    const reg = getRegExp(searchKeyword.value);
    const filterFn = field =>
      !shadowVisible.value.some(shadowField => shadowField.field_name === field.field_name) &&
      field.field_type !== '__virtual__' &&
      !excludesFields.includes(field.field_name) &&
      (reg.test(field.field_name) || reg.test(field.query_alias ?? ''));

    return fieldList.value.filter(filterFn);
  });

  const shadowVisible = ref([]);

  const dragOptions = ref({
    animation: 150,
    tag: 'ul',
    handle: '.bklog-drag-dots',
    'ghost-class': 'sortable-ghost-class',
  });

  // 计算属性
  const toSelectLength = computed(() => {
    return shadowTotal.value.length;
  });

  const fieldTypeMap = computed(() => store.state.globals.fieldTypeMap);
  const getFieldIcon = fieldType => {
    return fieldTypeMap.value?.[fieldType] ? fieldTypeMap.value?.[fieldType]?.icon : 'bklog-icon bklog-unkown';
  };

  const getFieldIconColor = type => {
    return fieldTypeMap.value?.[type] ? fieldTypeMap.value?.[type]?.color : '#EAEBF0';
  };

  // 新建提交逻辑
  const handleCreateRequest = async () => {
    const { common_filter_addition } = store.getters;
    const param = {
      filterSetting: shadowVisible.value,
      filterAddition: common_filter_addition.filter(item => shadowVisible.value.some(f => f.field_name === item.field)),
    };
    isLoading.value = true;

    store
      .dispatch('userFieldConfigChange', param)
      .then(res => {
        if (res.result) {
          window.mainComponent.messageSuccess($t('提交成功'));
        }
      })
      .finally(() => {
        isLoading.value = false;
      });
  };

  const confirmModifyFields = async () => {
    handleCreateRequest();
    fieldsSettingPopperRef?.value.instance.hide();
  };

  const fieldsSettingPopperRef = ref('');
  const cancelModifyFields = () => {
    fieldsSettingPopperRef?.value.instance.hide();
  };

  const addField = fieldInfo => {
    shadowVisible.value.push(fieldInfo);
  };

  const deleteField = (fieldName, index) => {
    shadowVisible.value.splice(index, 1);
  };

  const addAllField = () => {
    shadowTotal.value.forEach(fieldInfo => {
      if (!shadowVisible.value.includes(fieldInfo)) {
        shadowVisible.value.push(fieldInfo);
      }
    });
  };

  const deleteAllField = () => {
    shadowVisible.value = [];
  };

  const setDefaultFilterList = () => {
    shadowVisible.value = [];
    shadowVisible.value.push(...filterFieldsList.value);
  };

  const handlePopoverShow = () => {
    setDefaultFilterList();
  };
</script>

<style lang="scss">
  @import '../../../scss/mixins/scroller';

  .bklog-common-field-filter {
    .fields-list-container {
      display: flex;
      padding: 0;

      .total-fields-list,
      .visible-fields-list,
      .sort-fields-list {
        width: 350px;
        height: 340px;
        border: 1px solid #dcdee5;
        border-bottom: none;

        .text-action {
          font-size: 12px;
          color: #3a84ff;
          cursor: pointer;
        }

        .title {
          position: relative;
          display: flex;
          align-items: center;
          height: 41px;
          padding: 0 16px;
          line-height: 40px;
          color: #313238;
          background: #fafbfd;
          border-top: 1px solid #dcdee5;
          border-bottom: 1px solid #dcdee5;

          .bklog-info-fill {
            margin-left: 8px;
            font-size: 14px;
            color: #979ba5;
            outline: none;
          }

          .add-all,
          .clear-all {
            position: absolute;
            top: 0;
            right: 16px;
          }
        }

        .select-list {
          height: 255px;
          padding: 4px 0;
          overflow: auto;

          @include scroller;

          .select-item {
            display: inline-block;
            align-items: center;
            width: 100%;
            height: 32px;
            padding: 0 12px;
            overflow: hidden;
            line-height: 32px;
            text-overflow: ellipsis;
            white-space: nowrap;
            cursor: pointer;

            span {
              display: inline-flex;
            }

            .bklog-drag-dots {
              width: 18px;
              font-size: 14px;
              color: #979ba5;
              text-align: left;
              cursor: move;
            }

            &.sortable-ghost-class {
              background: #eaf3ff;
              transition: background 0.2s linear;
            }

            &:hover {
              background: #eaf3ff;
            }

            .field-type-icon {
              display: inline-flex;
              align-items: center;
              justify-content: center;
              width: 16px;
              height: 16px;
              background: #dcdee5;
              border-radius: 2px;

              &.full-text {
                position: relative;

                &::after {
                  position: absolute;
                  top: 1px;
                  left: 5px;
                  width: 4px;
                  height: 4px;
                  content: '*';
                }
              }

              &.bklog-ext {
                font-size: 8px;
              }
            }

            .field-alias {
              display: inline;
              padding: 0 4px;
              font-size: 12px;
              line-height: 20px;
              color: #63656e;
              letter-spacing: 0;
            }

            .field-name {
              font-size: 12px;
              font-weight: 400;
              line-height: 20px;
              color: #9b9da1;
              letter-spacing: 0;
            }
          }
        }
      }

      .total-fields-list {
        border-right: none;
      }

      .visible-fields-list {
        width: 380px;
        border-left: none;
      }

      /* stylelint-disable-next-line no-descending-specificity */
      .total-fields-list .select-list .select-item {
        position: relative;

        .field-name {
          display: inline;
        }

        .bklog-filled-right-arrow {
          position: absolute;
          top: 8px;
          right: 4px;
          z-index: 10;
          width: 24px;
          font-size: 16px;
          color: #3a84ff;
          text-align: right;
          cursor: pointer;
          opacity: 0;
          transition: opacity 0.2s linear;
          transform: scale(0.5);
          transform-origin: right center;
        }

        &:hover .bklog-filled-right-arrow {
          opacity: 1;
          transition: opacity 0.2s linear;
        }
      }

      .sort-fields-list {
        flex-shrink: 0;

        .sort-list-header {
          display: flex;
          align-items: center;
          height: 31px;
          font-size: 12px;
          line-height: 30px;
          background: rgba(250, 251, 253, 1);
          border-bottom: 1px solid rgba(221, 228, 235, 1);
        }

        /* stylelint-disable-next-line no-descending-specificity */
        .select-list .select-item {
          .field-name {
            // 16 42 50 38
            width: calc(100% - 146px);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }

          .status {
            font-weight: 700;

            &.icon-arrows-down-line {
              color: #ea3636;
            }

            &.icon-arrows-up-line {
              color: #2dcb56;
            }
          }

          .option {
            width: 50px;
            margin: 0 8px;
            color: #3a84ff;
          }

          .delete {
            font-size: 16px;
            color: #c4c6cc;
            text-align: right;
            cursor: pointer;
          }
        }
      }

      /* stylelint-disable-next-line no-descending-specificity */
      .visible-fields-list .select-list .select-item {
        position: relative;

        .field-name {
          display: inline;
        }
        
        .delete {

          position: absolute;
          top: 8px;
          right: 12px;
          display: none;
          font-size: 16px;
          color: #c4c6cc;
          text-align: right;
          cursor: pointer;
          }

        &:hover .delete {
          display: block;
        }
      }

      .sort-icon {
        display: flex;
        flex-shrink: 0;
        align-items: center;
        justify-content: center;
        width: 1px;
        background-color: #dcdee5;

        .bklog-double-arrow {

          position: absolute;

          display: flex;
          align-items: center;
          justify-content: center;

          width: 33px;
          height: 33px;
          font-size: 12px;
          color: #989ca5;

          pointer-events: none;
          background: #fafbfd;
          border-radius: 50%;
        }
      }
    }

    &.fields-button-container {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      width: 100%;
      height: 51px;
      padding: 0 24px;
      background-color: #fafbfd;
      border-top: 1px solid #dcdee5;
      border-radius: 0 0 2px 2px;
    }
  }

</style>
