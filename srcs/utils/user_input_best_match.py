import difflib


def user_input_best_match(enter: str, all_element: list, max_missing=2, search_break_weight_ratio=2):
    """match user input to str element in list, if success, a string will be returned"""
    # priority:
    # is whole word > block count > index_found > ratio
    # (1, 2, 40) < (1, 3, 1)
    # if in whole word, block count must = 1
    # let whole word = 0, and block count start from 1

    # min (- is whole word + block count + missing / x, -index, -ratio)
    enter = enter.replace('\\', '')
    results = {}
    matcher = difflib.SequenceMatcher(a=enter)

    for full_name in all_element:
        matcher.set_seq2(b=full_name)
        blocks = [i for i in matcher.get_matching_blocks() if i.size > 0]  # all match with len >= 1
        # print(f"{full_name}: {blocks}")
        if blocks:  # only if there is a match
            # include in result
            if enter in full_name.split():  # special case
                results[full_name] = [-1.0]
            else:
                size_matched = 0
                for block in blocks:
                    size_matched += block.size
                missing = len(enter) - size_matched  # 0 ~ len(enter)-1
                if missing > max_missing:  # too off
                    continue  # to next full name
                # the lesser len(block) is, the better
                # if len(block increases by 1, and missing decreases by 2, its balanced out
                # number of char is worth for 1 break here:   ↓
                results[full_name] = [len(blocks) + missing / search_break_weight_ratio]  # 0 ~ inf
            # index found
            results[full_name].append(blocks[0].b)  # 0~inf
            # ratio
            results[full_name].append(-matcher.quick_ratio())  # 0~0.9999

    # for result in sorted(results, key=lambda x: results[x], reverse=True):
    #     print(f"{result}: {results[result]}")
    if results:
        return min(results, key=lambda x: results[x])
    else:
        return None