/*
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
 */
import { onBeforeUnmount, onMounted, ref, Ref } from 'vue';

import { debounce } from 'lodash';

export default (
  target: Ref<HTMLElement>,
  callback: (entry: IntersectionObserverEntry) => void,
  options?: IntersectionObserverInit,
) => {
  let observer = null;
  const destroyObserver = () => {
    if (observer) {
      observer.disconnect();
      observer = null;
    }
  };
  const isIntersecting = ref(false);
  const debounceCallback = debounce((entry: IntersectionObserverEntry) => callback?.(entry));

  const createObserver = () => {
    observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          isIntersecting.value = entry.isIntersecting;
          debounceCallback(entry);
        });
      },
      {
        root: null,
        threshold: 0.01,
        ...(options ?? {}),
      },
    );

    if (target.value) {
      observer?.observe(target.value);
    }
  };

  onMounted(() => {
    createObserver();
  });

  onBeforeUnmount(() => {
    destroyObserver();
  });

  return { isIntersecting };
};