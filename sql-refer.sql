
####
Nth Highest Salary ####

CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
DECLARE M INT;
SET M=N-1;
  RETURN (
      # Write your MySQL query statement below.
      select distinct Salary
      from Employee
      order by salary desc limit m, 1   
      # LIMIT 5 OFFSET [Number of rows to skip]
      # LIMIT 5 OFFSET 3
      #  LIMIT 3 , 5    
  );
END

#### window function)
window_function_name(expression) OVER ( 
   [partition_defintion]
   [order_definition]
   [frame_definition]
)

######
185. Department Top Three Salaries
#Unlike the RANK() function, the DENSE_RANK() function always returns consecutive rank values.
#  SUM(sale) OVER (PARTITION BY fiscal_year) total_sales
#1 The DENSE_RANK() is a window function that assigns a rank to each row within a partition or result set with no gaps in ranking values.

Select D.Name as Department, 
       rank_tb.Name as Employee, 
       rank_tb.Salary
From  (SELECT *, 
    DENSE_RANK() OVER (PARTITION BY
                     DepartmentId
                 ORDER BY
                     Salary DESC
                ) salary_rank
                    FROM Employee e1) as rank_tb
JOIN Department D ON D.Id = rank_tb.DepartmentId 
WHERE rank_tb.salary_rank < 4

#2 
SELECT d.Name AS Department, e1.Name AS Employee, e1.Salary 
FROM Employee e1
left JOIN Department d 
ON e1.DepartmentID = d.Id
WHERE 3 > (select count(distinct(e2.Salary)) 
                  from Employee e2 
                  where e2.Salary > e1.Salary 
                  and e1.DepartmentId = e2.DepartmentId)


			
##### rank_over 			
# Write your MySQL query statement below
#SELECT C.customer_id, O.product_id, O.product_name
# Write an SQL query to find the most frequently ordered product(s) for each customer.

SELECT RES.customer_id, RES.product_id, RES.product_name
FROM (
    SELECT O.customer_id, O.product_id, p.product_name,
    # ADD ONE COLUMN FOR RANK 
            RANK() OVER (PARTITION BY 
                            O.customer_id 
                         ORDER BY 
                            COUNT(O.product_id) DESC) PROD_RANK
    FROM Orders O
    LEFT JOIN Products P
    ON O.product_id = P.product_id
    GROUP BY O.customer_id, O.product_id ) RES
WHERE RES.PROD_RANK = 1
			
			
			
			
			
####
Department Highest Salary

SELECT D.Name AS Department ,E.Name AS Employee ,E.Salary 
from 
	Employee E,
	Department D 
WHERE E.DepartmentId = D.id 
  AND (DepartmentId,Salary) in 
  (SELECT DepartmentId,max(Salary) as max FROM Employee GROUP BY DepartmentId)


#  Delete Duplicate Emails and keep only unique emails based on its smallest Id.
  DELETE p1 FROM Person p1,
    Person p2
WHERE
    p1.Email = p2.Email AND p1.Id > p2.Id


 #Trips and Users: Write a SQL query to find 
 #the cancellation rate of requests with unbanned users 
 #(both client and driver must not be banned) 
 #each day between "2013-10-01" and "2013-10-03".


 Select Request_at as Day,
        round(sum(case when Trips.Status != 'completed' then 1 else 0 end)/count(*),2) as 'Cancellation Rate'
From Trips    
Where Client_Id in (Select Users_Id from Users Where Banned= "No" AND Role = "client")
        AND Driver_Id in (Select Users_Id from Users Where Banned= "No" AND Role = "driver") 
        AND Request_at >= '2013-10-01' and Request_at <= '2013-10-03'
Group by Request_at


