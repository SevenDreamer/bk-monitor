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

<script setup>
  import { computed, ref, watch } from 'vue';

  import useStore from '@/hooks/use-store';
  import RouteUrlResolver, { RetrieveUrlResolver } from '@/store/url-resolver';
  import { debounce } from 'lodash';
  import { useRoute, useRouter } from 'vue-router/composables';

  import CollectFavorites from './collect/collect-index';
  import SearchBar from './search-bar/index.vue';
  import SearchResultPanel from './search-result-panel/index.vue';
  import SearchResultTab from './search-result-tab/index.vue';

  import GraphAnalysis from './search-result-panel/graph-analysis';
  import SubBar from './sub-bar/index.vue';

  import useResizeObserve from '../../hooks/use-resize-observe';
  import RetrieveHelper from '../retrieve-helper';
  import useRetrieveHook from './use-retrieve-hook';

  const store = useStore();
  const router = useRouter();
  const route = useRoute();

  const showFavorites = ref(false);
  const favoriteRef = ref(null);
  const favoriteWidth = ref(240);

  RetrieveHelper.setScrollSelector();
  const GLOBAL_SCROLL_SELECTOR = RetrieveHelper.getScrollSelector();

  const spaceUid = computed(() => store.state.spaceUid);
  const bkBizId = computed(() => store.state.bkBizId);

  const { search_mode, addition, keyword } = route.query;

  const { resolveQueryParams } = useRetrieveHook();
  resolveQueryParams({ search_mode, addition, keyword });

  /**
   * 拉取索引集列表
   */
  const getIndexSetList = () => {
    store.dispatch('retrieve/getIndexSetList', { spaceUid: spaceUid.value, bkBizId: bkBizId.value }).then(resp => {});
  };

  const handleSpaceIdChange = () => {
    store.commit('resetIndexsetItemParams');
    store.commit('updateIndexId', '');
    store.commit('updateUnionIndexList', []);
    getIndexSetList();
    store.dispatch('requestFavoriteList');
  };

  handleSpaceIdChange();

  watch(spaceUid, () => {
    handleSpaceIdChange();
    const routeQuery = route.query ?? {};

    if (routeQuery.spaceUid !== spaceUid.value) {
      const resolver = new RouteUrlResolver({ route });

      router.replace({
        params: {
          indexId: undefined,
        },
        query: {
          ...resolver.getDefUrlQuery(),
          spaceUid: spaceUid.value,
          bizId: bkBizId.value,
        },
      });
    }
  });

  const handleFavoritesClick = () => {
    if (showFavorites.value) return;
    showFavorites.value = true;
  };

  const handleFavoritesClose = e => {
    e.stopPropagation();
    showFavorites.value = false;
  };

  const handleEditFavoriteGroup = e => {
    e.stopPropagation();
    favoriteRef.value.isShowManageDialog = true;
  };

  const isRefreshList = ref(false);
  const searchBarHeight = ref(0);
  /** 刷新收藏夹列表 */
  const handleRefresh = v => {
    isRefreshList.value = v;
  };
  const handleHeightChange = height => {
    searchBarHeight.value = height;
  };

  const debounceUpdateTabValue = debounce(value => {
    const isClustering = value === 'clustering';
    router.replace({
      params: { ...(route.params ?? {}) },
      query: {
        ...(route.query ?? {}),
        tab: value,
        ...(isClustering ? {} : { clusterParams: undefined }),
      },
    });
  }, 60);

  const activeTab = computed({
    get() {
      return route.query.tab ?? 'origin';
    },
    set(val) {
      debounceUpdateTabValue(val);
    },
  });

  const stickyStyle = computed(() => {
    return {
      '--offset-search-bar': `${searchBarHeight.value + 8}px`,
    };
  });

  const contentStyle = computed(() => {
    return {
      '--left-width': `${showFavorites.value ? favoriteWidth.value : 0}px`,
    };
  });

  const showAnalysisTab = computed(() => activeTab.value === 'graphAnalysis');
  const activeFavorite = ref();
  const updateActiveFavorite = value => {
    activeFavorite.value = value;
  };

  /** 开始处理滚动容器滚动时，收藏夹高度 */

  // 顶部二级导航高度，这个高度是固定的
  const subBarHeight = ref(64);
  const paddingTop = ref(0);
  // 滚动容器高度
  const scrollContainerHeight = ref(0);

  RetrieveHelper.on(RetrieveEvent.GLOBAL_SCROLL, event => {
    const scrollTop = event.target.scrollTop;
    paddingTop.value = scrollTop > subBarHeight.value ? subBarHeight.value : scrollTop;
  });

  useResizeObserve(
    GLOBAL_SCROLL_SELECTOR,
    entry => {
      scrollContainerHeight.value = entry.target.offsetHeight;
    },
    0,
  );

  const favoritesStlye = computed(() => {
    const height = scrollContainerHeight.value - subBarHeight.value;
    if (showFavorites.value) {
      return {
        height: `${height + paddingTop.value}px`,
      };
    }

    return {};
  });

  const isStickyTop = computed(() => {
    return paddingTop.value === subBarHeight.value;
  });

  /*** 结束计算 ***/
</script>
<template>
  <div
    :style="stickyStyle"
    :class="['retrieve-v2-index', { 'show-favorites': showFavorites, 'scroll-y': true, 'is-sticky-top': isStickyTop }]"
  >
    <div class="sub-head">
      <div
        :style="{ width: `${showFavorites ? favoriteWidth : 42}px` }"
        class="box-favorites"
        @click="handleFavoritesClick"
      >
        <div
          v-if="showFavorites"
          class="collet-label"
        >
          <div class="left-info">
            <span class="collect-title">{{ $t('收藏夹') }}</span>
            <span class="collect-count">{{ favoriteRef?.allFavoriteNumber }}</span>
            <span
              class="collect-edit bklog-icon bklog-wholesale-editor"
              @click="handleEditFavoriteGroup"
            ></span>
          </div>
          <span
            class="bklog-icon bklog-collapse-small"
            @click="handleFavoritesClose"
          ></span>
        </div>
        <template v-else>
          <div class="collection-box">
            <span
              style="font-size: 18px"
              :class="['bklog-icon bklog-shoucangjia', { active: showFavorites }]"
            ></span>
          </div>
        </template>
      </div>
      <SubBar
        :style="{ width: `calc(100% - ${showFavorites ? favoriteWidth : 42}px` }"
        show-favorites
      />
    </div>
    <div
      :style="contentStyle"
      :class="['retrieve-v2-body']"
    >
      <CollectFavorites
        ref="favoriteRef"
        :style="favoritesStlye"
        class="collect-favorites"
        :is-refresh.sync="isRefreshList"
        :is-show.sync="showFavorites"
        :width.sync="favoriteWidth"
        @update-active-favorite="updateActiveFavorite"
      ></CollectFavorites>
      <div class="retrieve-v2-content">
        <SearchBar
          :active-favorite="activeFavorite"
          :show-favorites="showFavorites"
          @height-change="handleHeightChange"
          @refresh="handleRefresh"
        >
        </SearchBar>
        <SearchResultTab v-model="activeTab"></SearchResultTab>
        <template v-if="showAnalysisTab">
          <GraphAnalysis></GraphAnalysis>
        </template>
        <template v-else>
          <SearchResultPanel :active-tab.sync="activeTab"></SearchResultPanel>
        </template>
      </div>
    </div>
  </div>
</template>
<style lang="scss">
  @import './index.scss';
</style>
<style lang="scss">
  @import './segment-pop.scss';

  .retrieve-v2-index {
    .collection-box {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      background: #f0f1f5;
      border-radius: 2px;
    }
  }
</style>
