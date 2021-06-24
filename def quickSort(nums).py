def quickSort(nums):
    end = len (nums)
    if end > 1: # list > 1
        i = -1 # record the pivot location
        pivot = end-1 #pivot index
        for j in range (end-1):
            if nums[j] <= nums[pivot]:
                i += 1
                nums[j], nums[i] = nums[i], nums[j] # swap smaller
        nums[pivot], nums[i+1] = nums[i+1], nums[pivot]   # swap pivot
    # recuisive left     f
        nums[:i+1]=quickSort(nums[:i+1])
    # recruisive right
        nums[i+2:]=quickSort(nums[i+2:])
    return nums


class Solution:    
    def sortArray(self, nums: List[int]) -> List[int]:    
        nums = quickSort(nums)
        return nums
            