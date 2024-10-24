package Work.example.Work;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.*;

public class Tests {
    private EmployeeStorage employeeStorage;
    private EmployeeService employeeService;

    @BeforeEach
    void setup() {
        this.employeeStorage = new EmployeeStorage();
        this.employeeService = new EmployeeService(employeeStorage);
    }

    @Test
    void createEmployeeWithInvalidId() {
        // Test dodawania pracownika z nieprawidłowym ID
        var result = employeeService.addEmployee(0, 22, "Sprzedawca", Department.SALES);
        assertThat(result).isEqualTo(null);
    }

    @Test
    void createEmployeeWithValidData() {
        // Test dodawania nowego pracownika z poprawnymi danymi
        var result = employeeService.addEmployee(3, 3000, "Programista", Department.DEVELOPMENT);
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(3);
        assertThat(result.getPosition()).isEqualTo("Programista");
    }

    @Test
    void createEmployeeWithNullDepartment() {
        // Test dodawania pracownika bez działu (department = null)
        var result = employeeService.addEmployee(4, 2500, "Tester", null);
        assertThat(result).isEqualTo(null);
    }

    @Test
    void changeDepartmentWithInvalidId() {
        // Test zmiany działu dla nieprawidłowego ID
        var result = employeeService.changeDepartment(5, Department.SALES);
        assertThat(result).isEqualTo(null);
    }

    @Test
    void changeDepartmentWithValidId() {
        // Test zmiany działu dla istniejącego pracownika
        employeeService.addEmployee(3, 3000, "Programista", Department.IT);
        var result = employeeService.changeDepartment(3, Department.SALES);
        assertThat(result).isNotNull();
        assertThat(result.getDepartment()).isEqualTo(Department.SALES);
    }

    @Test
    void changePositionWithValidId() {
        // Test zmiany stanowiska dla istniejącego pracownika
        var result = employeeService.changePosition(1, "Menadżer");
        Employee expectedEmployee = new Employee(1, 22, "Menadżer", Department.SALES);
        assertThat(result.toString()).isEqualTo(expectedEmployee.toString());
    }

    @Test
    void changePositionWithInvalidId() {
        // Test zmiany stanowiska dla nieprawidłowego ID
        var result = employeeService.changePosition(99, "Klasy");
        assertThat(result).isEqualTo(null);
    }

    @Test
    void findEmployeeByIdThatExists() {
        // Test wyszukiwania pracownika o istniejącym ID
        var result = employeeService.findEmployee(1);
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1);
    }

    @Test
    void findEmployeeByIdThatDoesNotExist() {
        // Test wyszukiwania pracownika, który nie istnieje
        var result = employeeService.findEmployee(100);
        assertThat(result).isEqualTo(null);
    }

    @Test
    void changeDepartmentToNull() {
        // Test zmiany działu na null
        employeeService.addEmployee(3, 3000, "Programista", Department.IT);
        var result = employeeService.changeDepartment(3, null);
        assertThat(result.getDepartment()).isEqualTo(null);
    }
}
