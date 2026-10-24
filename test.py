def maximumUniqueSubarray(nums: list[int]) -> int:
    set1 = set()
    left = 0
    max_sum = 0
    curr_sum = 0

    for right in range(len(nums)):
        while nums[right] in set1:
            set1.remove(nums[left])
            curr_sum -= nums[left]
            left += 1

        set1.add(nums[right])
        curr_sum += nums[right]

        max_sum = max(max_sum, curr_sum)

    return max_sum


# Test the code
nums = [4, 2, 4, 5, 6]

answer = maximumUniqueSubarray(nums)

print("Array:", nums)
print("Maximum unique subarray sum:", answer)