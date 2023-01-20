package Work.example.Work;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class WorkApplication {

	public static void main(String[] args) {
		SpringApplication.run(WorkApplication.class, args);
	}
	public WorkApplication(EmployeeService employeeService){
		System.out.println(employeeService.addEmployee(3,13,"Sutener",Department.DEVELOPMENT));
		System.out.println(employeeService.findEmployee(3));
		System.out.println(employeeService.changeDepartment(3,Department.SALES));
		System.out.println(employeeService.changePosition(3,"Asystent"));
	}
}
